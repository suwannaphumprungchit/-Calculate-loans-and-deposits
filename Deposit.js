
// ============================================================
// deposit.js - ส่วนคำนวณเงินฝาก (ดอกเบี้ยทบต้น ฝากเพิ่มทุกงวด)
// ============================================================

// ส่วนที่ 1: ตรวจสอบค่าที่รับเข้ามา
function toNumber(value, name, minimum = 0, strict = false, maximum = null) {
    const v = Number(String(value).replace(/,/g, "").trim());

    if (String(value).trim() === "" || !Number.isFinite(v)) {
        throw new Error(`${name}: กรุณากรอกเป็นตัวเลข`);
    }

    if (strict ? v <= minimum : v < minimum) {
        throw new Error(
            `${name}: ต้อง${strict ? "มากกว่า" : "ไม่น้อยกว่า"} ${minimum.toLocaleString("th-TH")}`
        );
    }

    if (maximum !== null && v > maximum) {
        throw new Error(`${name}: ต้องไม่เกิน ${maximum.toLocaleString("th-TH")}`);
    }

    return v;
}


// ส่วนที่ 2: สูตรคำนวณเงินฝาก
function futureValue(P, i, n, D) {
    if (i === 0) {
        return P + D * n;
    }

    const growth = Math.pow(1 + i, n);

    return P * growth + D * (growth - 1) / i;
}


// ส่วนที่ 3: ฟังก์ชันคำนวณหลัก
function calculateDeposit(principal, years, add, rate, months) {

    const mo = toNumber(months, "รอบการฝาก (จำนวนเดือน)", 0, true, 1200);
    const P = toNumber(principal, "เงินต้น");
    const t = toNumber(years, "จำนวนปี", 0, true, 100);
    const D = toNumber(add, "เงินฝากเพิ่ม");
    const r = toNumber(rate, "อัตราดอกเบี้ย", 0, false, 100);

    // ดอกเบี้ยต่อหนึ่งงวด
    const i = r / 100 * mo / 12;

    // จำนวนงวดทั้งหมด
    const nExact = t * 12 / mo;
    const n = Math.round(nExact);

    if (n < 1) {
        throw new Error("จำนวนปี: สั้นเกินไป ไม่ครบ 1 งวด");
    }

    if (Math.abs(nExact - n) > 1e-6) {
        throw new Error(
            `จำนวนปี: ${t} ปี (${t * 12} เดือน) หารด้วยรอบ ${mo} เดือนไม่ลงตัว กรุณาปรับให้ลงตัว`
        );
    }

    // คำนวณเงินรวม
    const total = futureValue(P, i, n, D);

    // เงินฝากรวม
    const paidIn = P + D * n;

    // ดอกเบี้ยรวม
    const interest = total - paidIn;

    return {
        label: `${mo} เดือน`,
        n: n,
        paid_in: paidIn,
        interest: interest,
        total: total
    };
}

