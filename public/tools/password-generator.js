function generate() {
  const len=+document.getElementById('len').value;
  let chars='';
  if(document.getElementById('upper').checked) chars+='ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  if(document.getElementById('lower').checked) chars+='abcdefghijklmnopqrstuvwxyz';
  if(document.getElementById('nums').checked) chars+='0123456789';
  if(document.getElementById('sym').checked) chars+='!@#$%^&*()_-+=[]{}|;:,.<>?';
  let p=''; for(let i=0;i<len;i++) p+=chars[Math.floor(Math.random()*chars.length)];
  document.getElementById('result').textContent=p||'请至少选择一种字符类型';
}
generate();