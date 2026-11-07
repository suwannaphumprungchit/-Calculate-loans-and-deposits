
// ============================================================
// loan.js - โปรแกรมคำนวณเงินกู้ (ลดต้นลดดอก)
// ============================================================

const MAX_ROWS = 1200;


// ------------------------------------------------------------
// ส่วนที่ 1: ตรวจสอบค่าที่รับเข้ามา
// ------------------------------------------------------------
function loanToNumber(value, name, minimum = 0, strict = false, maximum = null) {

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


// ------------------------------------------------------------
// ส่วนที่ 2: สูตรคำนวณ
// ------------------------------------------------------------

// ค่างวดคงที่
function loanPayment(L, i, n) {

    if (i === 0) {
        return L / n;
    }

    return L * i / (1 - Math.pow(1 + i, -n));
}


// ยอดหนี้คงค้างหลังผ่อนไปแล้ว k งวด
function loanBalance(L, i, A, k) {

    if (i === 0) {
        return Math.max(L - A * k, 0);
    }

    const growth = Math.pow(1 + i, k);

    return Math.max(
        L * growth - A * (growth - 1) / i,
        0
    );
}


// ------------------------------------------------------------
// ส่วนที่ 3: ตรวจสอบข้อมูลเงินกู้
// ------------------------------------------------------------
function loanSetup(amount, years, rate, months) {

    const mo = loanToNumber(
        months, "รอบการผ่อน (จำนวนเดือน)", 0, true, 1200
    );

    const L = loanToNumber(amount, "เงินกู้", 0, true);

    const t = loanToNumber(
        years, "จำนวนปี", 0, true, 100
    );

    const r = loanToNumber(
        rate, "อัตราดอกเบี้ย", 0, false, 100
    );

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

    if (n > MAX_ROWS) {
        throw new Error(
            `จำนวนงวดมากเกินไป (เกิน ${MAX_ROWS} งวด) กรุณาลดจำนวนปี หรือเพิ่มรอบการผ่อน`
        );
    }

    return {
        L: L,
        i: i,
        n: n,
        label: `${mo} เดือน`
    };
}


// ------------------------------------------------------------
// ส่วนที่ 4: คำนวณเงินกู้และสร้างตารางผ่อนชำระ
// ------------------------------------------------------------
function calculateLoan(amount, years, rate, months) {

    const { L, i, n, label } = loanSetup(
        amount, years, rate, months
    );

    const A = loanPayment(L, i, n);

    const schedule = [];

    for (let k = 1; k <= n; k++) {

        const before = loanBalance(L, i, A, k - 1);

        const interestK = before * i;

        schedule.push({
            k: k,
            interest: interestK,
            principal: A - interestK,
            balance: loanBalance(L, i, A, k)
        });
    }

    return {
        label: label,
        n: n,
        payment: A,
        total_paid: A * n,
        interest: A * n - L,
        principal: L,
        schedule: schedule
    };
}


// ------------------------------------------------------------
// ส่วนที่ 5: คำนวณยอดหนี้คงเหลือ
// ------------------------------------------------------------
function balanceAfter(amount, years, rate, months, k) {

    const { L, i, n } = loanSetup(
        amount, years, rate, months
    );

    const value = String(k).trim();
    const kk = Number(value);

    if (
        value === "" ||
        !Number.isFinite(kk) ||
        !Number.isInteger(kk) ||
        kk < 0 ||
        kk > n
    ) {
        throw new Error(
            `จำนวนงวดที่ผ่อนไปแล้ว: กรุณากรอกจำนวนเต็มตั้งแต่ 0 ถึง ${n}`
        );
    }

    const A = loanPayment(L, i, n);

    return {
        k: kk,
        balance: loanBalance(L, i, A, kk)
    };
}
