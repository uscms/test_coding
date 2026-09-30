#!/usr/bin/env node
/**
 * renamer —— 批量重命名命令行工具（只用 Node 内置模块，无需 npm 安装）
 *
 * 用法：
 *   node renamer.js <目录> --prefix img-      给文件加前缀，并按序号排列
 *   node renamer.js <目录> --ext .jpg         只处理指定扩展名
 *   node renamer.js <目录> --dry              只打印计划，不真改名
 */
const fs = require('fs');
const path = require('path');

const argv = process.argv.slice(2);
if (!argv.length) {
  console.log('用法：node renamer.js <目录> [--prefix 前缀] [--ext .jpg] [--dry]');
  process.exit(1);
}
const dir = argv[0];
const flag = (name) => argv.includes(name);
const value = (name) => {
  const i = argv.indexOf(name);
  return i >= 0 && i + 1 < argv.length ? argv[i + 1] : null;
};

if (!fs.existsSync(dir) || !fs.statSync(dir).isDirectory()) {
  console.error('不是目录或不存在：' + dir);
  process.exit(1);
}

const prefix = value('--prefix') || 'file-';
const onlyExt = value('--ext');
const dry = flag('--dry');

let files = fs.readdirSync(dir).filter((f) => fs.statSync(path.join(dir, f)).isFile());
if (onlyExt) files = files.filter((f) => path.extname(f).toLowerCase() === onlyExt.toLowerCase());
files.sort();

console.log(dry ? '计划重命名（未实际执行）：\n' : '开始重命名：\n');
let n = 0;
files.forEach((f, i) => {
  const ext = path.extname(f);
  const next = prefix + String(i + 1).padStart(3, '0') + ext;
  if (next === f) return;
  const from = path.join(dir, f);
  const to = path.join(dir, next);
  if (fs.existsSync(to)) {
    console.log('  跳过（目标已存在）：' + f + ' -> ' + next);
    return;
  }
  if (!dry) fs.renameSync(from, to);
  console.log('  ' + f + '  ->  ' + next);
  n++;
});
console.log('\n' + (dry ? '预览' : '已完成') + ' ' + n + ' 个文件。');
