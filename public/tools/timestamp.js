function tsToDate(){const v=document.getElementById('ts').value;const d=new Date(v.length>10?v*1:v*1000);document.getElementById('ts-result').textContent=d.toLocaleString('zh-CN',{timeZone:'Asia/Shanghai'});}
function dateToTs(){const v=document.getElementById('dt').value;document.getElementById('ts-result').textContent='秒: '+Math.floor(new Date(v).getTime()/1000)+' | 毫秒: '+new Date(v).getTime();}
document.getElementById('current').textContent='当前时间戳(秒): '+Math.floor(Date.now()/1000);
const now=new Date();document.getElementById('dt').value=now.toISOString().slice(0,16);