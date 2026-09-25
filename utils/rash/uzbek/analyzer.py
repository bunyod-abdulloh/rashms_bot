import os

import numpy as np
from aiogram.types import InputFile
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    HRFlowable, Table, TableStyle
)

from data.config import ADMINS
from loader import bot, udb, rdb

users_dict = {}


# ==============================================================
# 1) RASCH — MINI JMLE (faqat kerak bo'lgan qismi)
# ==============================================================
def rasch_jmle(X, max_iter=600, lr=0.05, tol=1e-6):
    # X: 0/1/nan

    # Correct mask creation
    mask = ~np.isnan(X)
    mask = mask.astype(bool)  # <<< MUST
    Xf = np.where(mask, X, 0.0)  # <<< MUST: NaN → 0

    eps = 1e-4

    # PERSON LEVEL
    cnt = mask.sum(axis=1)
    sum_correct = Xf.sum(axis=1)

    # Avoid NaN in cnt
    cnt = np.where(cnt > 0, cnt, 1)

    prop = sum_correct / cnt
    prop = np.clip(prop, eps, 1 - eps)

    theta = np.log(prop / (1 - prop))
    theta -= theta.mean()

    # ITEM LEVEL
    cnt_i = mask.sum(axis=0)
    sum_correct_i = Xf.sum(axis=0)

    cnt_i = np.where(cnt_i > 0, cnt_i, 1)

    prop_i = sum_correct_i / cnt_i
    prop_i = np.clip(prop_i, eps, 1 - eps)

    b = -np.log(prop_i / (1 - prop_i))
    b -= b.mean()

    # ITERATION
    for _ in range(max_iter):
        prev = theta.copy()

        logits = np.clip(theta[:, None] - b[None, :], -20, 20)
        P = 1 / (1 + np.exp(-logits))

        diff = (Xf - P) * mask

        theta += lr * diff.sum(axis=1)
        b -= lr * diff.sum(axis=0)

        theta -= theta.mean()
        b -= b.mean()

        if np.max(np.abs(theta - prev)) < tol:
            break

    return theta


def to_T(theta):
    sd = theta.std()
    if sd <= 0:
        sd = 1
    return 50 + 10 * ((theta - theta.mean()) / sd)


# ==============================================================
# 2) DARAJA / FOIZ
# ==============================================================
def calc_percent(score):
    if score < 46:  return "--"
    if score >= 70: return str(100)
    if score >= 65: return str(round(score / 69.9 * 100, 1))
    if score >= 60: return str(round(score / 64.9 * 100, 1))
    if score >= 55: return str(round(score / 59.9 * 100, 1))
    if score >= 50: return str(round(score / 54.9 * 100, 1))
    if score >= 46: return str(round(score / 49.9 * 100, 1))
    return None


def calc_grade(score):
    if score >= 70: return "A+"
    if score >= 65: return "A"
    if score >= 60: return "B+"
    if score >= 55: return "B"
    if score >= 50: return "C+"
    if score >= 46: return "C"
    return "--"


# ==============================================================
# 3) GENERATE PDF
# ==============================================================
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


async def generate_test_pdf(results, test_name, test_code):
    # REGISTER FONT
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    FONT_PATH = os.path.join(
        BASE_DIR,
        "..",
        "fonts",
        "NotoSans-Regular.ttf"
    )
    FONT_PATH = os.path.abspath(FONT_PATH)

    pdfmetrics.registerFont(TTFont('NotoSans', FONT_PATH))

    filename = f"test_result_{test_code}.pdf"
    filepath = os.path.join("media", filename)
    os.makedirs("media", exist_ok=True)

    doc = SimpleDocTemplate(filepath, pagesize=A4,
                            leftMargin=35, rightMargin=35,
                            topMargin=40, bottomMargin=40)

    styles = getSampleStyleSheet()
    styles['Normal'].fontName = 'NotoSans'

    elements = []

    title = Paragraph(
        f"<para align='center'><b><font size=18>{test_name} natijalari</font></b></para>",
        styles['Normal']
    )
    subtitle = Paragraph(
        f"<para align='center'><font size=12 color='blue'>Test kodi: {test_code}</font></para>",
        styles['Normal']
    )

    elements += [
        title, Spacer(1, 14),
        subtitle, Spacer(1, 10),
        HRFlowable(width='100%', thickness=1, color=colors.grey),
        Spacer(1, 12)
    ]

    data = [["T/r", "F.I.SH", "Test", "Esse", "Umumiy", "Foiz", "Daraja"]]

    for i, r in enumerate(results, start=1):
        data.append([
            str(i),
            r["full_name"],
            r["t1"],
            r["t2"],
            str(r["rasch"]),
            f"{r['percent']} %",
            r["grade"],
        ])

    colWidths = [30, 200, 70, 45, 45, 55, 45, 50]
    t = Table(data, colWidths=colWidths)

    style = [
        ('FONTNAME', (0, 0), (-1, -1), 'NotoSans'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e6e6e6")),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]

    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor("#f7f7f7")))

    t.setStyle(TableStyle(style))
    elements.append(t)

    doc.build(elements)

    return filepath


# ==============================================================
# 4) ASOSIY FUNKSIYA — SIZGA KERAK BO‘LGAN YAGONA NARSALAR
# ==============================================================
async def analyze_results(test_code_id):
    data = await rdb.get_results(test_code_id=test_code_id)

    if not data:
        await bot.send_message(ADMINS[0], "⚠️ Test topilmadi!")
        return

    # ----------------------------
    # 1) USER & QUESTION INDEX
    # ----------------------------
    users = sorted({d["telegram_id"] for d in data})
    questions = sorted({d["question_number"] for d in data})

    U = len(users)
    Q = len(questions)

    user_idx = {u: i for i, u in enumerate(users)}
    ques_idx = {q: j for j, q in enumerate(questions)}

    # ----------------------------
    # 2) RASCH MATRIX (1–44)
    # ----------------------------
    X = np.full((U, Q), np.nan)

    for d in data:
        q = str(d["question_number"])
        if q:
            i = user_idx[d["telegram_id"]]
            j = ques_idx[q]
            X[i, j] = 1 if d["correct_answer"] else 0

    # ----------------------------
    # 3) RASCH SCORE (t1)
    # ----------------------------
    theta1 = rasch_jmle(X)
    t1 = to_T(theta1)
    t1 = np.clip(t1, 0, 75)

    # ----------------------------
    # 4) ESSE BALL (t2)
    # ----------------------------
    essay_balls = await rdb.get_essay_ball(test_code_id)
    score_map = {a["telegram_id"]: float(a["essay_ball"]) for a in essay_balls}

    t2 = np.zeros(U)
    for uid, i in user_idx.items():
        t2[i] = score_map.get(uid, 0.0)

    t2 = np.clip(t2, 0, 75)

    # ----------------------------
    # 5) FINAL SCORE — ikkala bo'limning arifmetik o'rtachasi (0-75 shkalada)
    # ----------------------------
    final = t1 + t2
    rasch = np.round(final / 2, 1)

    # ----------------------------
    # 6) NATIJALAR
    # ----------------------------
    all_users = await udb.get_all_users_dict()

    grade_counts = {
        "A+": 0, "A": 0, "B+": 0, "B": 0,
        "C+": 0, "C": 0, "Olmaganlar": 0,
    }

    results = []

    for i, uid in enumerate(users):
        score = float(rasch[i])
        grade = calc_grade(score)

        if grade == "A+":
            grade_counts["A+"] += 1
        elif grade == "A":
            grade_counts["A"] += 1
        elif grade == "B+":
            grade_counts["B+"] += 1
        elif grade == "B":
            grade_counts["B"] += 1
        elif grade == "C+":
            grade_counts["C+"] += 1
        elif grade == "C":
            grade_counts["C"] += 1
        else:
            grade_counts["Olmaganlar"] += 1

        fullname = all_users.get(uid, None)[0]
        pupil_id = all_users.get(uid, None)[1]
        teacher_id = all_users.get(uid, None)[2]

        if fullname:
            results.append({
                "test_id": test_code_id,
                "pupil_id": pupil_id,
                "full_name": fullname,
                "teacher_id": teacher_id,
                "t1": round(float(t1[i]), 1),
                "t2": round(float(t2[i]), 1),
                "rasch": score,
                "percent": calc_percent(score),
                "grade": grade,
            })
    print(results)
    results = sorted(results, key=lambda x: x["full_name"] or "")

    await rdb.bulk_add_rash_results(results)

    # ----------------------------
    # 7) PDF
    # ----------------------------
    test_code = await rdb.get_test_code(test_code_id=test_code_id)
    pdf_path = await generate_test_pdf(results, test_name="Test", test_code=test_code)

    # ----------------------------
    # 8) ADMIN
    # ----------------------------
    caption_text = (
        f"🏁 Test yakunlandi!\n\n"
        f"🔖 Kod: {test_code}\n"
        f"❓ Savollar soni: {Q}\n"
        f"👥 Qatnashuvchilar: {len(results)} ta\n\n"
        f"📊 Darajalar:\n\n"
        f"🏆 A+ — {grade_counts['A+']}\n"
        f"🥇 A  — {grade_counts['A']}\n"
        f"🥈 B+ — {grade_counts['B+']}\n"
        f"🥉 B  — {grade_counts['B']}\n"
        f"🎓 C+ — {grade_counts['C+']}\n"
        f"📘 C  — {grade_counts['C']}\n"
        f"❌ Olmaganlar — {grade_counts['Olmaganlar']}\n\n"
    )

    try:
        await bot.send_document(
            chat_id=ADMINS[0],
            document=InputFile(pdf_path),
            caption=caption_text
        )
        # await bot.send_document(
        #     chat_id=ADMINS[1],
        #     document=InputFile(pdf_path),
        #     caption=caption_text
        # )
        os.remove(pdf_path)
    except Exception as err:
        await bot.send_message(chat_id=ADMINS[0], text=f"PDF yuborishda xatolik:\n{err}")