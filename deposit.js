// deposit.js - โปรแกรมคำนวณเงินฝาก (ดอกเบี้ยทบต้น ฝากเพิ่มทุกรอบ)
// วิธีรัน: node deposit.js
const readline = require("readline/promises");

async function calculateSavings() {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

  console.log("\n--- Savings Calculator ---");
  let p = parseFloat(await rl.question("Enter the initial deposit amount: "));
  const r = parseFloat(await rl.question("Enter the annual interest rate (percent): "));
  const m = parseFloat(await rl.question("Enter the deposit amount per period: "));
  const k = parseFloat(await rl.question("Deposit and compound every how many months (e.g. 1, 3, 6, 10): "));
  const totalMonths = parseFloat(await rl.question("Enter the total number of months: "));
  rl.close();

  if ([p, r, m, k, totalMonths].some(Number.isNaN) || k <= 0 || totalMonths <= 0) {
    console.log("Invalid input. Please enter numbers only (period and total months must be more than 0).");
    return;
  }

  // จำนวนงวดเต็ม: ไม่ต้องหารลงตัว ถ้ามีเดือนเหลือไม่ครบงวดจะไม่นับ
  const n = Math.floor(totalMonths / k + 1e-9);
  if (n < 1) {
    console.log(`Total months (${totalMonths}) is less than one period (${k} months).`);
    return;
  }

  const i = (r / 100) * (k / 12); // ดอกเบี้ยต่อ 1 งวด

  for (let j = 1; j <= n; j++) {
    p = p * (1 + i) + m;
    console.log(`Month ${+(j * k).toFixed(6)}: ${p.toFixed(2)}`);
  }

  const usedMonths = +(n * k).toFixed(6);
  console.log(`\nTotal savings after ${usedMonths} months: ${p.toFixed(2)}`);

  const leftover = +(totalMonths - usedMonths).toFixed(6);
  if (leftover > 0) {
    console.log(`Note: ${totalMonths} months is not a multiple of ${k}. ` +
      `${n} full periods were counted; the remaining ${leftover} month(s) were not counted.`);
  }
}

calculateSavings();