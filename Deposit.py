# -*- coding: utf-8 -*-
"""
Deposit.py  -  ส่วนคำนวณ "เงินฝาก" (ดอกเบี้ยทบต้น ฝากเพิ่มทุกงวด)

ไฟล์นี้ใช้ได้ 2 แบบ
  1) รันตรง ๆ ในหน้าจอดำ:   python Deposit.py
  2) ถูกเรียกใช้โดย server.py เมื่อกดปุ่มคำนวณในหน้าเว็บ index.html

สูตร (ที่มาอยู่ในไฟล์ PDF):  A_n = P(1+i)^n + D * ((1+i)^n - 1) / i
  P = เงินต้น, D = ฝากเพิ่มต่องวด (ปลายงวด), i = ดอกเบี้ยต่องวด, n = จำนวนงวด
"""
import math


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
def future_value(P, i, n, D):
    """เงินรวมเมื่อสิ้นงวดที่ n"""
    if i == 0:                       # ไม่มีดอกเบี้ย สูตรหารด้วย 0 ไม่ได้
        return P + D * n
    growth = (1 + i) ** n
    return P * growth + D * (growth - 1) / i


def calculate(principal, years, add, rate, months):
    """
    รับค่าจากลูกค้า แล้วคืนผลลัพธ์เป็น dict
      principal = เงินต้น (บาท)        years  = ฝากกี่ปี
      add       = ฝากเพิ่มต่องวด (บาท)  rate   = ดอกเบี้ยต่อปี (%)
      months    = รอบการฝากเพิ่มและคิดดอกเบี้ยทุกกี่เดือน (เช่น 1, 3, 6, 12)
    """
    mo = to_number(months, "รอบการฝาก (จำนวนเดือน)", strict=True, maximum=1200)
    P = to_number(principal, "เงินต้น")
    t = to_number(years, "จำนวนปี", strict=True, maximum=100)
    D = to_number(add, "เงินฝากเพิ่ม")
    r = to_number(rate, "อัตราดอกเบี้ย", maximum=100)

    i = r / 100 * mo / 12            # ดอกเบี้ยต่อ 1 งวด (1 งวด = mo เดือน)
    n_exact = t * 12 / mo            # จำนวนงวดทั้งหมด
    n = round(n_exact)
    if n < 1:
        raise ValueError("จำนวนปี: สั้นเกินไป ไม่ครบ 1 งวด")
    if abs(n_exact - n) > 1e-6:
        raise ValueError(f"จำนวนปี: {t:g} ปี ({t * 12:g} เดือน) หารด้วยรอบ {mo:g} เดือน ไม่ลงตัว กรุณาปรับให้ลงตัว")

    total = future_value(P, i, n, D)
    paid_in = P + D * n
    return {
        "label": f"{mo:g} เดือน",
        "n": n,
        "paid_in": paid_in,
        "interest": total - paid_in,
        "total": total,
    }


# ------------------------------------------------------------
# ส่วนที่ 3: โหมดพิมพ์ถามตอบในหน้าจอดำ (รันด้วย python Deposit.py)
# ------------------------------------------------------------
def ask(prompt, convert):
    """ถามซ้ำจนกว่าจะกรอกถูก convert คือฟังก์ชันตรวจค่า"""
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
    print("  โปรแกรมคำนวณเงินฝาก (ดอกเบี้ยทบต้น)")
    print("=" * 50)
    while True:
        months = ask("\nฝากเพิ่มและคิดดอกเบี้ยทุกกี่เดือน (เช่น 1, 3, 6, 12): ",
                     lambda s: to_number(s, "รอบการฝาก (จำนวนเดือน)", strict=True, maximum=1200))
        label = f"{months:g} เดือน"

        principal = ask("1) ต้องการฝากเงินต้นเท่าไหร่ (บาท): ", lambda s: to_number(s, "เงินต้น"))
        years = ask("2) จะฝากไปโดยไม่ถอนกี่ปี: ", lambda s: to_number(s, "จำนวนปี", strict=True, maximum=100))
        add = ask(f"3) จะฝากเพิ่มทุก {label} ครั้งละเท่าไหร่ (บาท, ไม่ฝากเพิ่มใส่ 0): ", lambda s: to_number(s, "เงินฝากเพิ่ม"))
        rate = ask("   อัตราดอกเบี้ยต่อปี (%): ", lambda s: to_number(s, "อัตราดอกเบี้ย", maximum=100))

        try:
            r = calculate(principal, years, add, rate, months)
        except ValueError as err:
            print("  !!", err)
            continue

        print("\n----- ผลลัพธ์ -----")
        print(f"จำนวนงวดทั้งหมด      : {r['n']} งวด (ทุก {r['label']})")
        print(f"เงินที่ฝากรวม        : {r['paid_in']:,.2f} บาท")
        print(f"ดอกเบี้ยรวมที่ได้    : {r['interest']:,.2f} บาท")
        print(f"เงินรวมสิ้นสุดการฝาก : {r['total']:,.2f} บาท")

        if not ask_yes_no("\nมีลูกค้าท่านต่อไปหรือไม่? (y/n): "):
            break
    print("\nขอบคุณที่ใช้บริการ")


if __name__ == "__main__":
    main()