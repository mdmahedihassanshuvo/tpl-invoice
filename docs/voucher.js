const source = document.getElementById('voucher-source');
const fields = [...source.querySelectorAll('[data-field]')];
const logo = document.getElementById('logo');
const defaultLogo = 'tigerpark-logo-full.svg';
const storageKey = 'tpl-payment-voucher-draft';

function refresh() {
  source.querySelectorAll('.date-shell').forEach(shell => {
    shell.querySelector('.date-display').textContent = shell.querySelector('input').value;
  });
  for (const type of ['debit', 'credit']) {
    const value = source.querySelector(`[data-field="${type}"]`).value;
    document.getElementById(`total-${type}`).textContent = value ? Number(value).toFixed(2) : '';
  }
}

source.addEventListener('input', refresh);
source.querySelectorAll('.voucher-date').forEach(input => {
  input.addEventListener('click', () => { if (input.showPicker) input.showPicker(); });
  input.addEventListener('change', refresh);
});

function snapshot() {
  return {fields: Object.fromEntries(fields.map(input => [input.dataset.field, input.value])), logo: logo.src};
}

function restore(data) {
  fields.forEach(input => { input.value = data.fields?.[input.dataset.field] || ''; });
  logo.src = data.logo || defaultLogo;
  refresh();
}

try { const saved = localStorage.getItem(storageKey); if (saved) restore(JSON.parse(saved)); } catch (_) { /* Storage may be unavailable. */ }

document.getElementById('new').addEventListener('click', () => {
  if (!confirm('Clear the current voucher?')) return;
  localStorage.removeItem(storageKey);
  restore({fields: {}, logo: defaultLogo});
  document.getElementById('logo-upload').value = '';
});

document.getElementById('save').addEventListener('click', () => {
  try { localStorage.setItem(storageKey, JSON.stringify(snapshot())); alert('Voucher saved in this browser.'); }
  catch (_) { alert('Could not save in this browser. Try a smaller logo.'); }
});

document.getElementById('logo-upload').addEventListener('change', function () {
  const file = this.files[0];
  if (!file) return;
  if (!['image/png', 'image/jpeg'].includes(file.type) || file.size > 1024 * 1024) { alert('Choose a PNG or JPEG logo under 1 MB.'); this.value = ''; return; }
  const reader = new FileReader();
  reader.onload = () => { logo.src = reader.result; };
  reader.readAsDataURL(file);
});

const escapeCell = value => String(value || '').replace(/\|/g, '\\|').replace(/\r?\n/g, ' ');
document.getElementById('markdown').addEventListener('click', () => {
  const v = snapshot().fields;
  const text = `# Payment Voucher\n\n**Tiger Park Limited**  \n2-16, Pallabi, Mirpur, Dhaka-1216, Bangladesh.  \nCell: 01517327315\n\nDate: ${v.date || ''}  \nVoucher No: ${v.voucher_no || ''}  \nDepartment: ${v.department || ''}  \nBank: ${v.bank || ''}  \nLedger No: ${v.ledger_no || ''}  \nCheque No: ${v.cheque_no || ''}  \nCash: ${v.cash || ''}  \nPay To: ${v.pay_to || ''}\n\n| Date | Payment Method | Ref No | Description | Dr (BDT) | Cr (BDT) | Sign |\n|---|---|---|---|---:|---:|---|\n| ${[v.line_date,v.payment_method,v.ref_no,v.description,v.debit,v.credit,v.signature].map(escapeCell).join(' | ')} |\n\nAmount in Words: ${v.amount_words || ''}\n\nPrepare By: ${v.prepared_by || ''}  \nReceived By: ${v.received_by || ''}  \nChecked By: ${v.checked_by || ''}  \nApprove By: ${v.approved_by || ''}\n`;
  const url = URL.createObjectURL(new Blob([text], {type: 'text/markdown'}));
  const link = document.createElement('a'); link.href = url; link.download = 'payment-voucher.md'; link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});

function buildPrint() {
  refresh();
  const target = document.getElementById('print-page'); target.replaceChildren();
  for (let i = 0; i < 2; i++) {
    const slot = document.createElement('div'); slot.className = 'print-slot';
    const copy = source.cloneNode(true);
    const originals = source.querySelectorAll('input'); const copies = copy.querySelectorAll('input');
    originals.forEach((input, index) => { copies[index].value = input.value; });
    slot.appendChild(copy); target.appendChild(slot);
  }
}
document.getElementById('print').addEventListener('click', () => { buildPrint(); window.print(); });
window.addEventListener('beforeprint', buildPrint);
refresh();
