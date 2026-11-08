// loan.js - โปรแกรมคำนวณเงินกู้ (ลดต้นลดดอก ผ่อนคงที่ทุกเดือน)
// วิธีรัน: node loan.js
const readline = require("readline/promises");

async function calculateLoan() {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

  console.log("\n--- Loan Payment Calculator ---");
  const l = parseFloat(await rl.question("Enter the loan amount: "));
  const r = parseFloat(await rl.question("Enter the annual interest rate (percent): "));
  const n = parseInt(await rl.question("Enter the number of months to repay: "), 10);
  rl.close();

  if ([l, r, n].some(Number.isNaN) || n < 1) {
    console.log("Invalid input. Please enter numbers only (months must be at least 1).");
    return;
  }

  const mr = r / 100 / 12; // ดอกเบี้ยต่อเดือน
  // ถ้าดอกเบี้ย 0% สูตรจะหารด้วย 0 ไม่ได้ จึงใช้ เงินกู้ / จำนวนเดือน
  const mp = mr === 0 ? l / n : (l * (mr * (1 + mr) ** n)) / ((1 + mr) ** n - 1);

  console.log(`\nYour monthly payment is: ${mp.toFixed(2)}`);

  const tp = mp * n;
  const ti = tp - l;

  console.log(`Total payment after ${n} months: ${tp.toFixed(2)}`);
  console.log(`Total interest paid: ${ti.toFixed(2)}`);
}

calculateLoan();
