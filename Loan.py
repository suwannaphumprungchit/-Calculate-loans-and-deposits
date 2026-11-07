# -*- coding: utf-8 -*-
"""
loan.py  -  ส่วนคำนวณ "เงินกู้" (ลดต้นลดดอก ผ่อนคงที่ทุกงวด)

ไฟล์นี้ใช้ได้ 2 แบบ
  1) รันตรง ๆ ในหน้าจอดำ:   python loan.py
  2) ถูกเรียกใช้โดย server.py เมื่อกดปุ่มคำนวณในหน้าเว็บ index.html

สูตร (ที่มาอยู่ในไฟล์ PDF)
  ค่างวด            A   = L*i / (1 - (1+i)^(-n))
  หนี้คงค้างหลังผ่อน k งวด  B_k = L(1+i)^k - A*((1+i)^k - 1)/i
  L = เงินกู้, i = ดอกเบี้ยต่องวด, n = จำนวนงวดทั้งหมด
"""
import math

MAX_ROWS = 1200   # จำกัดจำนวนงวดไม่ให้ตารางใหญ่เกินไป


# ------------------------------------------------------------
# ส่วนที่ 1: ตรวจสอบค่าที่รับเข้ามา
# ------------------------------------------------------------
def to_number(value, name, minimum=0.0, strict=False, maximum=None):
    """แปลงข้อความเป็นตัวเลข ถ้าไม่ถูกต้องจะแจ้งข้อผิดพลาดเป็นภาษาไทย (ValueError)"""
    try:
        v = float(str(value).replace(",", "").strip())
    except ValueError:
        raise ValueError(f"{name}: กรุณากรอกเป็นตัวเลข")
    if not math.isfinite(v):
        raise ValueError(f"{name}: กรุณากรอกเป็นตัวเลข")
    if (v <= minimum) if strict else (v < minimum):
        raise ValueError(f"{name}: ต้อง{'มากกว่า' if strict else 'ไม่น้อยกว่า'} {minimum:,.0f}")
    if maximum is not None and v > maximum:
        raise ValueError(f"{name}: ต้องไม่เกิน {maximum:,.0f}")
    return v


# ------------------------------------------------------------
# ส่วนที่ 2: สูตรคำนวณ
# ------------------------------------------------------------
def loan_payment(L, i, n):
    """ค่างวดคงที่"""
    if i == 0:
        return L / n
    return L * i / (1 - (1 + i) ** (-n))


def loan_balance(L, i, A, k):
    """ยอดหนี้คงค้างหลังผ่อนไปแล้ว k งวด (ไม่ให้ติดลบจากการปัดเศษ)"""
    if i == 0:
        return max(L - A * k, 0.0)
    growth = (1 + i) ** k
    return max(L * growth - A * (growth - 1) / i, 0.0)


def setup(amount, years, rate, months):
    """ตรวจค่าที่กรอก แล้วคืน (L, i, n, label)  โดย 1 งวด = months เดือน"""
    mo = to_number(months, "รอบการผ่อน (จำนวนเดือน)", strict=True, maximum=1200)
    L = to_number(amount, "เงินกู้", strict=True)
    t = to_number(years, "จำนวนปี", strict=True, maximum=100)
    r = to_number(rate, "อัตราดอกเบี้ย", maximum=100)
    i = r / 100 * mo / 12            # ดอกเบี้ยต่อ 1 งวด
    n_exact = t * 12 / mo            # จำนวนงวดทั้งหมด
    n = round(n_exact)
    if n < 1:
        raise ValueError("จำนวนปี: สั้นเกินไป ไม่ครบ 1 งวด")
    if abs(n_exact - n) > 1e-6:
        raise ValueError(f"จำนวนปี: {t:g} ปี ({t * 12:g} เดือน) หารด้วยรอบ {mo:g} เดือน ไม่ลงตัว กรุณาปรับให้ลงตัว")
    if n > MAX_ROWS:
        raise ValueError(f"จำนวนงวดมากเกินไป (เกิน {MAX_ROWS} งวด) กรุณาลดจำนวนปี หรือเพิ่มรอบการผ่อน")
    return L, i, n, f"{mo:g} เดือน"


def calculate(amount, years, rate, months):
    """
    คืนผลลัพธ์เป็น dict: ค่างวด, ยอดจ่ายรวม, ดอกเบี้ยรวม และตารางผ่อนชำระทุกงวด
      amount = เงินกู้ (บาท)   years = ผ่อนให้หมดในกี่ปี
      rate   = ดอกเบี้ยต่อปี (%)   months = ผ่อนทุกกี่เดือน (เช่น 1, 3, 6, 12)
    """
    L, i, n, label = setup(amount, years, rate, months)
    A = loan_payment(L, i, n)

    schedule = []
    for k in range(1, n + 1):
        before = loan_balance(L, i, A, k - 1)
        interest_k = before * i
        schedule.append({
            "k": k,
            "interest": interest_k,
            "principal": A - interest_k,
            "balance": loan_balance(L, i, A, k),
        })
    return {
        "label": label,
        "n": n,
        "payment": A,
        "total_paid": A * n,
        "interest": A * n - L,
        "principal": L,
        "schedule": schedule,
    }


def balance_after(amount, years, rate, months, k):
    """ยอดหนี้คงค้างหลังผ่อนไปแล้ว k งวด"""
    L, i, n, label = setup(amount, years, rate, months)
    try:
        kk = float(str(k).strip())
    except ValueError:
        raise ValueError("จำนวนงวดที่ผ่อนไปแล้ว: กรุณากรอกเป็นจำนวนเต็ม")
    if kk != int(kk) or kk < 0 or kk > n:
        raise ValueError(f"จำนวนงวดที่ผ่อนไปแล้ว: กรุณากรอกจำนวนเต็มตั้งแต่ 0 ถึง {n}")
    kk = int(kk)
    A = loan_payment(L, i, n)
    return {"k": kk, "balance": loan_balance(L, i, A, kk)}


# ------------------------------------------------------------
# ส่วนที่ 3: โหมดพิมพ์ถามตอบในหน้าจอดำ (รันด้วย python loan.py)
# ------------------------------------------------------------
def ask(prompt, convert):
    while True:
        try:
            return convert(input(prompt))
        except ValueError as err:
            print("  !!", err)


def ask_yes_no(prompt):
    while True:
        a = input(prompt).strip().lower()
        if a in ("y", "yes", "ใช่"):
            return True
        if a in ("n", "no", "ไม่"):
            return False
        print("  !! กรุณาพิมพ์ y (ใช่) หรือ n (ไม่ใช่)")


def main():
    print("=" * 50)
    print("  โปรแกรมคำนวณเงินกู้ (ลดต้นลดดอก)")
    print("=" * 50)
    while True:
        months = ask("\nผ่อนชำระทุกกี่เดือน (เช่น 1, 3, 6, 12): ",
                     lambda s: to_number(s, "รอบการผ่อน (จำนวนเดือน)", strict=True, maximum=1200))

        amount = ask("1) ต้องการกู้เงินต้นเท่าไหร่ (บาท): ", lambda s: to_number(s, "เงินกู้", strict=True))
        years = ask("2) จะผ่อนให้หมดในกี่ปี: ", lambda s: to_number(s, "จำนวนปี", strict=True, maximum=100))
        rate = ask("3) ธนาคารคิดดอกเบี้ยต่อปี (%): ", lambda s: to_number(s, "อัตราดอกเบี้ย", maximum=100))

        try:
            r = calculate(amount, years, rate, months)
        except ValueError as err:
            print("  !!", err)
            continue

        print("\n----- ผลลัพธ์ -----")
        print(f"ต้องผ่อนทุก {r['label']} งวดละ : {r['payment']:,.2f} บาท")
        print(f"จำนวนงวดทั้งหมด        : {r['n']} งวด")
        print(f"ยอดจ่ายรวมทั้งหมด      : {r['total_paid']:,.2f} บาท")
        print(f"ดอกเบี้ยรวมที่จ่าย     : {r['interest']:,.2f} บาท")

        while ask_yes_no("\nต้องการดูยอดหนี้คงค้างหลังผ่อนไปแล้ว k งวดหรือไม่? (y/n): "):
            k = ask(f"  ผ่อนไปแล้วกี่งวด (0 ถึง {r['n']}): ",
                    lambda s: balance_after(amount, years, rate, months, s))
            print(f"  ยอดหนี้คงค้างหลังผ่อน {k['k']} งวด = {k['balance']:,.2f} บาท")

        if not ask_yes_no("\nมีลูกค้าท่านต่อไปหรือไม่? (y/n): "):
            break
    print("\nขอบคุณที่ใช้บริการ")


if __name__ == "__main__":
    main()