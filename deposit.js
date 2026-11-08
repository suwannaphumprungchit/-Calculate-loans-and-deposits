// deposit.js - เงินฝากดอกเบี้ยทบต้น ใช้ผลเฉลยทั่วไปของความสัมพันธ์เวียนเกิด
// a_n = (1+i)a_{n-1} + k  ->  a_n = (1+i)^n * a0 + k * ((1+i)^n - 1) / i
const readline = require("readline/promises");

// ผลเฉลยทั่วไป: คำนวณ a_n โดยตรง
//ประกาศฟังก์ชันชื่อ  รับค่า 4 ตัว
//a0 = เงินฝากเริ่มต้น
//i = อัตราดอกเบี้ยต่อ 1 งวด (เป็นทศนิยม เช่น 0.01 = 1%)
//k = เงินฝากเพิ่มทุกงวด
//n = จำนวนงวด

function solve(a0, i, k, n) {
  if (i === 0) return a0 + n * k;             // กรณี i = 0
  const g = Math.pow(1 + i, n);              //คำนวณ (1+i)ⁿ เก็บไว้ในตัวแปร g
  return g * a0 + (k * (g - 1)) / i;        // คืนค่าตามสูตร aₙ = (1+i)ⁿ·a₀ + k·((1+i)ⁿ − 1)/i
}

//รับข้อมูลจากผู้ใช้งาน
async function calculateSavings() {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

  console.log("\n--- Savings Calculator ---");
  const a0 = parseFloat(await rl.question("Enter the initial deposit amount (a0): "));
  const r = parseFloat(await rl.question("Enter the annual interest rate (percent): "));
  const k = parseFloat(await rl.question("Enter the deposit amount per period (k): "));
  const months = parseFloat(await rl.question("Deposit and compound every how many months (e.g. 1, 3, 6, 10): "));
  const totalMonths = parseFloat(await rl.question("Enter the total number of months: "));
  rl.close();

  if ([a0, r, k, months, totalMonths].some(Number.isNaN) || months <= 0 || totalMonths <= 0) {
    console.log("Invalid input. Please enter numbers only (period and total months must be more than 0).");
    return;
  }

  // จำนวนงวดเต็ม n (ไม่ต้องหารลงตัว เดือนที่เหลือไม่ครบงวดจะไม่นับ)
  const n = Math.floor(totalMonths / months + 1e-9);
  if (n < 1) {
    console.log(`Total months (${totalMonths}) is less than one period (${months} months).`);
    return;
  }

  const i = (r / 100) * (months / 12); // อัตราดอกเบี้ยต่อ 1 งวด (เป็นทศนิยม)

  console.log(`\nPeriod rate i = ${(i * 100).toFixed(4)}%  |  n = ${n} periods`);
  for (let j = 1; j <= n; j++) {
    console.log(`Month ${+(j * months).toFixed(6)}: ${solve(a0, i, k, j).toFixed(2)}`);
  }

  const usedMonths = +(n * months).toFixed(6);
  console.log(`\nTotal savings after ${usedMonths} months: ${solve(a0, i, k, n).toFixed(2)}`);

  const leftover = +(totalMonths - usedMonths).toFixed(6);
  if (leftover > 0) {
    console.log(`Note: ${totalMonths} months is not a multiple of ${months}. ` +
      `${n} full periods were counted; the remaining ${leftover} month(s) were not counted.`);
  }
}

calculateSavings();