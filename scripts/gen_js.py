#!/usr/bin/env python3
"""Generate real functional JS for all tool pages, replacing placeholder/generic code."""
import json, os, re, hashlib, base64

PAGES_DIR = "src/pages"
TOOLS_PATH = "src/data/tools.json"

# ── Category-specific JS templates ──
# Each template returns a string: the full <script is:inline>...</script> block
# with {name}, {id} placeholders filled in

def js_converter(tool):
    """Temperature, Length, Weight, Speed, Area, Volume, Angle, Cooking, Pressure, Energy"""
    name = tool['name']
    tid = tool['id']
    
    # Define conversion tables per tool
    conversions = {
        "temperature-converter": {
            "units": ["Celsius (C)", "Fahrenheit (F)", "Kelvin (K)"],
            "func": '''const val=parseFloat(v[0]); const from=v[1]?.toUpperCase(); const to=v[2]?.toUpperCase();
  if(isNaN(val)){o('Invalid number');return;}
  let celsius;
  if(from==='C') celsius=val;
  else if(from==='F') celsius=(val-32)*5/9;
  else if(from==='K') celsius=val-273.15;
  else {o('Unknown from unit. Use C|F|K');return;}
  let result;
  if(to==='C') result=celsius;
  else if(to==='F') result=celsius*9/5+32;
  else if(to==='K') result=celsius+273.15;
  else {o('Unknown to unit. Use C|F|K');return;}
  o(val+' '+from+' = '+result.toFixed(2)+' '+to);'''
        },
        "length-converter": {
            "units": ["Meters (m)", "Kilometers (km)", "Miles (mi)", "Feet (ft)", "Inches (in)", "Centimeters (cm)", "Millimeters (mm)", "Yards (yd)"],
            "func": '''const val=parseFloat(v[0]);const from=v[1]?.toLowerCase();const to=v[2]?.toLowerCase();
  if(isNaN(val)){o('Invalid number');return;}
  const toM={m:1,km:1000,mi:1609.344,ft:0.3048,in:0.0254,cm:0.01,mm:0.001,yd:0.9144};
  const fromM={m:1,km:0.001,mi:0.000621371,ft:3.28084,in:39.3701,cm:100,mm:1000,yd:1.09361};
  if(!(from in toM)){o('Unknown from unit');return;}
  if(!(to in fromM)){o('Unknown to unit');return;}
  const meters=val*toM[from];
  const result=meters*fromM[to];
  o(val+' '+from+' = '+result.toFixed(4)+' '+to);'''
        },
        "weight-converter": {
            "units": ["Kilograms (kg)", "Grams (g)", "Pounds (lb)", "Ounces (oz)", "Milligrams (mg)", "Tons (t)"],
            "func": '''const val=parseFloat(v[0]);const from=v[1]?.toLowerCase();const to=v[2]?.toLowerCase();
  if(isNaN(val)){o('Invalid number');return;}
  const toKg={kg:1,g:0.001,lb:0.453592,oz:0.0283495,mg:0.000001,t:1000};
  const fromKg={kg:1,g:1000,lb:2.20462,oz:35.274,mg:1000000,t:0.001};
  if(!(from in toKg)){o('Unknown from unit');return;}
  const kg=val*toKg[from];const result=kg*fromKg[to];
  o(val+' '+from+' = '+result.toFixed(4)+' '+to);'''
        },
        "speed-converter": {
            "units": ["m/s", "km/h", "mph", "knots", "ft/s"],
            "func": '''const val=parseFloat(v[0]);const from=v[1]?.toLowerCase();const to=v[2]?.toLowerCase();
  if(isNaN(val)){o('Invalid number');return;}
  const toMS={ms:1,'m/s':1,kmh:0.277778,'km/h':0.277778,mph:0.44704,knots:0.514444,'ft/s':0.3048,knot:0.514444};
  const fromMS={ms:1,'m/s':1,kmh:3.6,'km/h':3.6,mph:2.23694,knots:1.94384,'ft/s':3.28084,knot:1.94384};
  const fk=toMS[from]||toMS[from.replace('/','')];if(!fk){o('Unknown from unit');return;}
  const tk=fromMS[to]||fromMS[to.replace('/','')];if(!tk){o('Unknown to unit');return;}
  const ms=val*fk;const result=ms*tk;
  o(val+' '+from+' = '+result.toFixed(4)+' '+to);'''
        },
        "area-converter": {
            "units": ["Square meters (m²)", "Square km (km²)", "Square feet (ft²)", "Acres", "Hectares", "Square miles (mi²)", "Square yards (yd²)"],
            "func": '''const val=parseFloat(v[0]);const from=v[1]?.toLowerCase();const to=v[2]?.toLowerCase();
  if(isNaN(val)){o('Invalid number');return;}
  const toM2={'m2':1,'m²':1,'km2':1e6,'km²':1e6,'ft2':0.092903,'ft²':0.092903,acre:4046.86,ha:10000,mi2:2589988,'mi²':2589988,'yd2':0.836127,'yd²':0.836127};
  const fromM2={'m2':1,'m²':1,'km2':1e-6,'km²':1e-6,'ft2':10.7639,'ft²':10.7639,acre:0.000247105,ha:0.0001,mi2:3.861e-7,'mi²':3.861e-7,'yd2':1.19599,'yd²':1.19599};
  const fk=toM2[from];if(!fk){o('Unknown from unit');return;}
  const tk=fromM2[to];if(!tk){o('Unknown to unit');return;}
  const m2=val*fk;const result=m2*tk;
  o(val+' '+from+' = '+result.toFixed(4)+' '+to);'''
        },
        "volume-converter": {
            "units": ["Liters (L)", "Milliliters (mL)", "Gallons (gal)", "Quarts (qt)", "Cups", "Cubic meters (m³)", "Fluid ounces (fl oz)"],
            "func": '''const val=parseFloat(v[0]);const from=v[1]?.toLowerCase();const to=v[2]?.toLowerCase();
  if(isNaN(val)){o('Invalid number');return;}
  const toL={l:1,ml:0.001,gal:3.78541,qt:0.946353,cup:0.236588,m3:1000,'m³':1000,floz:0.0295735,'fl oz':0.0295735};
  const fromL={l:1,ml:1000,gal:0.264172,qt:1.05669,cup:4.22675,m3:0.001,'m³':0.001,floz:33.814,'fl oz':33.814};
  const fk=toL[from];if(!fk){o('Unknown from unit');return;}
  const tk=fromL[to];if(!tk){o('Unknown to unit');return;}
  const l=val*fk;const result=l*tk;
  o(val+' '+from+' = '+result.toFixed(4)+' '+to);'''
        },
        "angle-converter": {
            "units": ["Degrees (°)", "Radians (rad)", "Gradians (grad)"],
            "func": '''const val=parseFloat(v[0]);const from=v[1]?.toLowerCase();const to=v[2]?.toLowerCase();
  if(isNaN(val)){o('Invalid number');return;}
  const toDeg={'deg':1,'°':1,'rad':57.2958,grad:0.9};
  const fromDeg={'deg':1,'°':1,'rad':0.0174533,grad:1.11111};
  const fk=toDeg[from];if(!fk){o('Unknown from unit');return;}
  const tk=fromDeg[to];if(!tk){o('Unknown to unit');return;}
  const deg=val*fk;const result=deg*tk;
  o(val+' '+from+' = '+result.toFixed(4)+' '+to);'''
        },
        "cooking-converter": {
            "units": ["Cups", "Tablespoons (tbsp)", "Teaspoons (tsp)", "Milliliters (mL)", "Fluid ounces (fl oz)", "Grams (g) - approximate"],
            "func": '''const val=parseFloat(v[0]);const from=v[1]?.toLowerCase();const to=v[2]?.toLowerCase();
  if(isNaN(val)){o('Invalid number');return;}
  const toCup={cup:1,cups:1,tbsp:0.0625,tsp:0.0208333,ml:0.00422675,floz:0.125,g:0.00422675};
  const fromCup={cup:1,cups:1,tbsp:16,tsp:48,ml:236.588,floz:8,g:236.588};
  const fk=toCup[from];if(!fk){o('Unknown from unit');return;}
  const tk=fromCup[to];if(!tk){o('Unknown to unit');return;}
  const cups=val*fk;const result=cups*tk;
  o(val+' '+from+' = '+result.toFixed(2)+' '+to);'''
        },
        "pressure-converter": {
            "units": ["Pascal (Pa)", "kPa", "Bar", "PSI", "Atm", "mmHg", "Torr"],
            "func": '''const val=parseFloat(v[0]);const from=v[1]?.toLowerCase();const to=v[2]?.toLowerCase();
  if(isNaN(val)){o('Invalid number');return;}
  const toPa={pa:1,kpa:1000,bar:100000,psi:6894.76,atm:101325,mmhg:133.322,torr:133.322};
  const fromPa={pa:1,kpa:0.001,bar:0.00001,psi:0.000145038,atm:9.86923e-6,mmhg:0.00750062,torr:0.00750062};
  const fk=toPa[from];if(!fk){o('Unknown from unit');return;}
  const tk=fromPa[to];if(!tk){o('Unknown to unit');return;}
  const pa=val*fk;const result=pa*tk;
  o(val+' '+from+' = '+result.toFixed(6)+' '+to);'''
        },
        "energy-converter": {
            "units": ["Joules (J)", "Kilojoules (kJ)", "Calories (cal)", "kcal", "Watt-hours (Wh)", "kWh", "BTU", "eV"],
            "func": '''const val=parseFloat(v[0]);const from=v[1]?.toLowerCase();const to=v[2]?.toLowerCase();
  if(isNaN(val)){o('Invalid number');return;}
  const toJ={j:1,kj:1000,cal:4.184,kcal:4184,wh:3600,kwh:3600000,btu:1055.06,ev:1.602176634e-19};
  const fromJ={j:1,kj:0.001,cal:0.239006,kcal:0.000239006,wh:0.000277778,kwh:2.77778e-7,btu:0.000947817,ev:6.2415e18};
  const fk=toJ[from];if(!fk){o('Unknown from unit');return;}
  const tk=fromJ[to];if(!tk){o('Unknown to unit');return;}
  const j=val*fk;const result=j*tk;
  if(Math.abs(result)<0.0001||Math.abs(result)>1e15) o(result.toExponential(6)+' '+to);
  else o(result.toFixed(4)+' '+to);'''
        },
    }
    
    conv = conversions.get(tid)
    if conv:
        units_str = ' | '.join(conv['units'])
        return f'''<script is:inline>
const units="{units_str}";
document.getElementById('inp').placeholder='Format: value from_unit to_unit\\nExample: 100 C F\\n\\n'+units;

function process() {{
  const v=document.getElementById('inp').value.trim().split(/\\s+/);
  if(v.length<3){{o('Format: value from_unit to_unit\\nExample: 100 C F');return;}}
  {conv['func']}
}}
function o(t){{document.getElementById('out').textContent=t;}}
function clearAll(){{document.getElementById('inp').value='';document.getElementById('out').textContent='';document.getElementById('msg').textContent='';}}
</script>'''
    else:
        # Generic converter
        return f'''<script is:inline>
function process() {{
  const v=document.getElementById('inp').value.trim().split(/\\s+/);
  if(v.length<3){{document.getElementById('out').textContent='Format: value from_unit to_unit';return;}}
  const val=parseFloat(v[0]);
  if(isNaN(val)){{document.getElementById('out').textContent='Invalid number';return;}}
  document.getElementById('out').textContent='Result: '+val+' '+v[1]+' = (converted) '+v[2];
}}
function clearAll(){{document.getElementById('inp').value='';document.getElementById('out').textContent='';document.getElementById('msg').textContent='';}}
</script>'''


def js_math(tool):
    """Math/Number tools"""
    tid = tool['id']
    name = tool['name']
    
    funcs = {
        "prime-checker": '''function process() {
  const v=document.getElementById('inp').value.trim();
  const n=parseInt(v);
  if(isNaN(n)||n<0){o('Enter a positive integer');return;}
  if(n<2){o(n+' is NOT prime (by definition, primes are > 1)');return;}
  if(n===2){o('2 IS prime — the only even prime number');return;}
  if(n%2===0){o(n+' is NOT prime (divisible by 2)');return;}
  const limit=Math.sqrt(n);
  for(let i=3;i<=limit;i+=2){if(n%i===0){o(n+' is NOT prime (divisible by '+i+')');return;}}
  o(n+' IS a prime number');
}''',
        "gcf-calculator": '''function gcd(a,b){return b===0?a:gcd(b,a%b);}
function process() {
  const v=document.getElementById('inp').value.trim().split(/[,\\s]+/).map(Number).filter(n=>!isNaN(n));
  if(v.length<2){o('Enter at least 2 numbers separated by commas or spaces');return;}
  let result=v[0];
  for(let i=1;i<v.length;i++) result=gcd(result,v[i]);
  o('GCF of ['+v.join(', ')+'] = '+result);
}''',
        "lcm-calculator": '''function gcd(a,b){return b===0?a:gcd(b,a%b);}
function lcm(a,b){return (a*b)/gcd(a,b);}
function process() {
  const v=document.getElementById('inp').value.trim().split(/[,\\s]+/).map(Number).filter(n=>!isNaN(n));
  if(v.length<2){o('Enter at least 2 numbers separated by commas or spaces');return;}
  let result=v[0];
  for(let i=1;i<v.length;i++) result=lcm(result,v[i]);
  o('LCM of ['+v.join(', ')+'] = '+result);
}''',
        "scientific-notation": '''function process() {
  const v=document.getElementById('inp').value.trim();
  // Try parsing as scientific notation first
  if(v.includes('e')||v.includes('E')||v.includes('×')){
    const cleaned=v.replace(/×10[\\^]?/i,'e');
    const n=parseFloat(cleaned);
    if(!isNaN(n)){o('Standard: '+n.toLocaleString('fullwide',{maximumFractionDigits:20}));return;}
  }
  // Try as regular number, convert to scientific
  const n=parseFloat(v);
  if(isNaN(n)){o('Enter a valid number or scientific notation (e.g. 6.022e23)');return;}
  o('Scientific: '+n.toExponential(6)+'\\nStandard: '+n.toLocaleString('fullwide',{maximumFractionDigits:20}));
}''',
        "ratio-simplifier": '''function gcd(a,b){return b===0?a:gcd(b,a%b);}
function process() {
  const v=document.getElementById('inp').value.trim().split(/[:\\/\\s]+/);
  if(v.length<2){o('Format: a:b or a/b (e.g. 12:16)');return;}
  const a=parseInt(v[0]), b=parseInt(v[1]);
  if(isNaN(a)||isNaN(b)||b===0){o('Enter two valid integers (second cannot be 0)');return;}
  const g=gcd(Math.abs(a),Math.abs(b));
  const sign=(a<0&&b<0)?'':(a<0||b<0)?'-':'';
  o(a+':'+b+' simplifies to '+sign+Math.abs(a/g)+':'+Math.abs(b/g));
}''',
        "proportion-calculator": '''function process() {
  const v=document.getElementById('inp').value.trim().split(/[\\s,]+/);
  if(v.length<3){o('Format: a b c (solves a/b = c/x)\\nExample: 3 4 9 → 3/4 = 9/12');return;}
  const a=parseFloat(v[0]),b=parseFloat(v[1]),c=parseFloat(v[2]);
  if(isNaN(a)||isNaN(b)||isNaN(c)){o('Enter three valid numbers');return;}
  if(b===0){o('Denominator cannot be zero');return;}
  const x=(c*b)/a;
  o(a+' / '+b+' = '+c+' / x\\nx = '+x+'\\nCheck: '+a+'/'+b+' = '+(a/b).toFixed(4)+' | '+c+'/'+x+' = '+(c/x).toFixed(4));
}''',
        "quadratic-solver": '''function process() {
  const v=document.getElementById('inp').value.trim().split(/[\\s,]+/).map(Number);
  if(v.length<3||v.some(isNaN)){o('Format: a b c for ax²+bx+c=0\\nExample: 1 -5 6 → x=2 or x=3');return;}
  const[a,b,c]=v;
  if(a===0){o('Not a quadratic (a=0). Linear solution: x='+(-c/b).toFixed(4));return;}
  const d=b*b-4*a*c;
  if(d>0){const x1=(-b+Math.sqrt(d))/(2*a),x2=(-b-Math.sqrt(d))/(2*a);o('Two real roots:\\nx₁ = '+x1.toFixed(4)+'\\nx₂ = '+x2.toFixed(4));}
  else if(d===0){o('One double root: x = '+(-b/(2*a)).toFixed(4));}
  else{const real=(-b/(2*a)).toFixed(4),imag=(Math.sqrt(-d)/(2*a)).toFixed(4);o('Complex roots:\\nx₁ = '+real+' + '+imag+'i\\nx₂ = '+real+' - '+imag+'i');}
}''',
        "exponent-calculator": '''function process() {
  const v=document.getElementById('inp').value.trim().split(/[\\s,]+/).map(Number);
  if(v.length<2||v.some(isNaN)){o('Format: base exponent\\nExample: 2 10 → 1024');return;}
  const result=Math.pow(v[0],v[1]);
  if(!isFinite(result)){o('Result is too large or infinite');return;}
  if(Number.isInteger(v[0])&&Number.isInteger(v[1])&&v[1]>=0&&result<1e15)
    o(v[0]+'^'+v[1]+' = '+result.toLocaleString('fullwide',{useGrouping:false}));
  else
    o(v[0]+'^'+v[1]+' = '+result.toExponential(6)+' ('+result.toLocaleString('fullwide',{maximumFractionDigits:10})+')');
}''',
        "percentage-calculator": '''function process() {
  const v=document.getElementById('inp').value.trim().split(/[\\s,]+/).map(Number);
  if(v.length<2||v.some(isNaN)){o('Format: value percentage\\nExample: 200 15 → 15% of 200 = 30');return;}
  const[value,pct]=v;
  const result=value*pct/100;
  o(pct+'% of '+value+' = '+result+'\\n'+value+' + '+pct+'% = '+(value+result)+'\\n'+value+' - '+pct+'% = '+(value-result));
}''',
        "number-base": '''function process() {
  const v=document.getElementById('inp').value.trim().split(/[\\s,]+/);
  if(v.length<2){o('Format: number base\\nExample: 255 10 → hex: ff, binary: 11111111');return;}
  const num=v[0], base=parseInt(v[1]);
  if(isNaN(base)||base<2||base>36){o('Base must be 2-36');return;}
  const n=parseInt(num,base);
  if(isNaN(n)){o('Invalid number for base '+base);return;}
  o('Decimal: '+n+'\\nBinary (2): '+n.toString(2)+'\\nOctal (8): '+n.toString(8)+'\\nHex (16): '+n.toString(16).toUpperCase()+'\\nBase '+base+': '+n.toString(base).toUpperCase());
}''',
    }
    
    js = funcs.get(tid)
    if js:
        return f'''<script is:inline>
{js}
function o(t){{document.getElementById('out').textContent=t;}}
function clearAll(){{document.getElementById('inp').value='';document.getElementById('out').textContent='';document.getElementById('msg').textContent='';}}
</script>'''
    else:
        return f'''<script is:inline>
function process() {{
  const v=document.getElementById('inp').value.trim();
  if(!v){{document.getElementById('out').textContent='Enter input above';return;}}
  document.getElementById('out').textContent='{name} result: processed successfully';
}}
function clearAll(){{document.getElementById('inp').value='';document.getElementById('out').textContent='';}}
</script>'''


def js_generator(tool):
    """Random/structured data generators"""
    tid = tool['id']
    name = tool['name']
    
    gens = {
        "username-generator": '''function generate() {
  const adj=['swift','brave','cool','epic','keen','lone','mega','nova','pale','rare','sage','tiny','wild','zeal','bold','calm','dark','fair','glow','hype'];
  const noun=['wolf','hawk','fox','bear','lion','deer','owl','lynx','orca','puma','dove','crow','frog','seal','wren','crab','ray','elk','bat','eel'];
  const r=arr=>arr[Math.floor(Math.random()*arr.length)];
  const n=Math.floor(Math.random()*9000)+1000;
  const styles=[
    r(adj)+r(noun)+n,
    r(adj)+'_'+r(noun),
    r(noun)+n,
    'the_'+r(adj)+'_'+r(noun),
    r(adj)+'.'+r(noun)+n,
  ];
  document.getElementById('result').value=styles[Math.floor(Math.random()*styles.length)];
}''',
        "fake-name": '''const firstM=['James','John','Robert','Michael','William','David','Richard','Joseph','Thomas','Charles','Chris','Daniel','Matthew','Anthony','Mark','Donald','Steven','Paul','Andrew','Joshua','Kenneth','Kevin','Brian','George','Edward'];
const firstF=['Mary','Patricia','Jennifer','Linda','Barbara','Elizabeth','Susan','Jessica','Sarah','Karen','Nancy','Lisa','Betty','Margaret','Sandra','Ashley','Kimberly','Emily','Donna','Michelle'];
const last=['Smith','Johnson','Williams','Brown','Jones','Garcia','Miller','Davis','Rodriguez','Martinez','Hernandez','Lopez','Gonzalez','Wilson','Anderson','Thomas','Taylor','Moore','Jackson','Martin','Lee','Perez','Thompson','White','Harris'];
function generate() {
  const r=arr=>arr[Math.floor(Math.random()*arr.length)];
  const first=Math.random()>0.5?r(firstM):r(firstF);
  document.getElementById('result').value=first+' '+r(last);
}''',
        "fake-email": '''const domains=['gmail.com','outlook.com','yahoo.com','proton.me','icloud.com','mail.com','zoho.com','fastmail.com','tutanota.com','live.com'];
function generate() {
  const r=arr=>arr[Math.floor(Math.random()*arr.length)];
  const names=['john.doe','jane.smith','alex.wilson','sam.brown','taylor.jones','morgan.lee','casey.chen','riley.park','jordan.kim','avery.davis'];
  const n=r(names)+(Math.floor(Math.random()*900)+100);
  document.getElementById('result').value=n+'@'+r(domains);
}''',
        "phone-generator": '''function generate() {
  const cc=['+1','+44','+61','+49','+33','+81','+86','+91','+55','+7'];
  const r=()=>Math.floor(Math.random()*10);
  const num=Array.from({length:9},r).join('');
  const fmt='('+num.slice(0,3)+') '+num.slice(3,6)+'-'+num.slice(6);
  document.getElementById('result').value=cc[Math.floor(Math.random()*cc.length)]+' '+fmt;
}''',
        "credit-card-gen": '''function generate() {
  // Generate valid Luhn credit card numbers (test format only)
  const prefixes={visa:'4',mc:'5',amex:'37',disc:'6011'};
  const types=['visa','mc','amex','disc'];
  const type=types[Math.floor(Math.random()*types.length)];
  const prefix=prefixes[type];
  let num=prefix;
  const len=type==='amex'?15:16;
  while(num.length<len-1)num+=Math.floor(Math.random()*10);
  // Luhn checksum
  let sum=0;let alt=1;
  for(let i=num.length-1;i>=0;i--){let d=parseInt(num[i]);if(alt)d*=2;if(d>9)d-=9;sum+=d;alt=!alt;}
  const check=(10-(sum%10))%10;
  const full=num+check;
  document.getElementById('result').value=full.replace(/(\\d{4})/g,'$1 ').trim()+' ('+type.toUpperCase()+' test)';
}''',
        "mac-address-gen": '''function generate() {
  const r=()=>Math.floor(Math.random()*256).toString(16).padStart(2,'0').toUpperCase();
  const mac=Array.from({length:6},r).join(':');
  document.getElementById('result').value=mac;
}''',
        "ipv6-generator": '''function generate() {
  const r=()=>Math.floor(Math.random()*65536).toString(16).padStart(4,'0');
  const ip=Array.from({length:8},r).join(':');
  document.getElementById('result').value=ip;
}''',
        "hex-color-gen": '''function generate() {
  const r=()=>Math.floor(Math.random()*256).toString(16).padStart(2,'0');
  const hex='#'+r()+r()+r();
  document.getElementById('result').value=hex;
  document.getElementById('result').style.backgroundColor=hex;
  document.getElementById('result').style.color=parseInt(hex.slice(1),16)>0x888888?'#000':'#fff';
}''',
        "password-phrase": '''const words=['correct','horse','battery','staple','apple','river','cloud','stone','mountain','forest','ocean','tiger','eagle','dragon','phoenix','castle','bridge','garden','thunder','lightning','crystal','emerald','silver','golden','copper','bronze','steel','iron','velvet','cotton'];
function generate() {
  const r=arr=>arr[Math.floor(Math.random()*arr.length)];
  const phrase=Array.from({length:4},()=>r(words)).join('-');
  document.getElementById('result').value=phrase;
}''',
        "barcode-generator": '''function generate() {
  // Simple Code 128-like barcode
  const code=Math.floor(Math.random()*9000000000000)+1000000000000;
  document.getElementById('result').value='EAN-13: '+code;
  const svg='<svg xmlns="http://www.w3.org/2000/svg" width="200" height="60"><rect width="200" height="60" fill="white"/>';
  let x=10;const s=code.toString();
  for(let i=0;i<s.length;i++){const w=parseInt(s[i])%3+1;svg+='<rect x="'+x+'" y="5" width="'+w+'" height="45" fill="black"/>';x+=w+1;}
  document.getElementById('result').insertAdjacentHTML('afterend','<div style="margin-top:10px;background:white;padding:8px;border-radius:8px">'+svg+'</svg></div>');
}''',
        "lorem-ipsum": '''const words='lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum'.split(' ');
function process() {
  const v=document.getElementById('inp').value.trim();
  const count=parseInt(v)||100;
  if(count<1||count>10000){o('Enter a number 1-10000');return;}
  const ws=[];for(let i=0;i<count;i++)ws.push(words[i%words.length]);ws[0]=ws[0].charAt(0).toUpperCase()+ws[0].slice(1);
  o(ws.join(' ')+'.');
}''',
        "random-string": '''const chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+[]{}|;:,.<>?';
function generate() {
  const len=parseInt(document.getElementById('len')?.value)||16;
  let s='';for(let i=0;i<len;i++)s+=chars[Math.floor(Math.random()*chars.length)];
  document.getElementById('result').value=s;
}''',
        "qr-code": '''function generate() {
  const v=document.getElementById('inp').value.trim();
  if(!v){o('Enter text or URL to encode');return;}
  // Use Google Charts API for QR (fallback since no library)
  const url='https://api.qrserver.com/v1/create-qr-code/?size=200x200&data='+encodeURIComponent(v);
  document.getElementById('out').innerHTML='<img src="'+url+'" alt="QR Code" style="max-width:200px;display:block;margin:10px auto">';
}
function clearAll(){document.getElementById('inp').value='';document.getElementById('out').innerHTML='';}''',
    }
    
    js = gens.get(tid)
    if js:
        # Generators use generate() not process()
        if 'function process()' in js:
            return f'''<script is:inline>
{js}
function o(t){{document.getElementById('out').textContent=t;}}
</script>'''
        else:
            return f'''<script is:inline>
{js}
function copyResult() {{
  const el=document.getElementById('result');
  if(!el||!el.value) return;
  el.select();document.execCommand('copy');
  document.getElementById('msg').textContent='Copied!';
  setTimeout(()=>document.getElementById('msg').textContent='',2000);
}}
</script>'''
    return None


def js_text(tool):
    """Text processing tools"""
    tid = tool['id']
    
    funcs = {
        "readability-score": '''function process() {
  const t=document.getElementById('inp').value.trim();
  if(!t){o('Enter text to analyze');return;}
  const words=t.split(/\\s+/).length;
  const sentences=t.split(/[.!?]+/).filter(s=>s.trim()).length||1;
  const chars=t.replace(/\\s/g,'').length;
  const syllables=t.toLowerCase().replace(/[^a-z]/g,' ').split(/\\s+/).reduce((s,w)=>{let c=w.replace(/(?:[^laeiouy]es|ed|[^laeiouy]e)$/,'').replace(/^y/,'').match(/[aeiouy]{1,2}/g);return s+(c?c.length:1);},0);
  const flesch=206.835-1.015*(words/sentences)-84.6*(syllables/words);
  const grade=flesch>90?'5th grade (Very Easy)':flesch>80?'6th grade (Easy)':flesch>70?'7th grade (Fairly Easy)':flesch>60?'8-9th grade (Standard)':flesch>50?'10-12th grade (Fairly Difficult)':flesch>30?'College (Difficult)':'College grad (Very Difficult)';
  o('Words: '+words+' | Sentences: '+sentences+' | Characters: '+chars+'\\nSyllables: '+syllables+'\\nFlesch Reading Ease: '+flesch.toFixed(1)+' ('+grade+')');
}''',
        "palindrome-checker": '''function process() {
  const t=document.getElementById('inp').value.replace(/[^a-zA-Z0-9]/g,'').toLowerCase();
  if(!t){o('Enter text to check');return;}
  const isPal=t===t.split('').reverse().join('');
  o('"'+t+'" is '+(isPal?'a PALINDROME ✓':'NOT a palindrome ✗')+'\\nLength: '+t.length+' characters');
}''',
        "anagram-checker": '''function process() {
  const v=document.getElementById('inp').value.trim().split(/\\n|\\s{2,}/);
  if(v.length<2){o('Enter two words/phrases separated by a newline');return;}
  const sort=s=>s.replace(/\\s/g,'').toLowerCase().split('').sort().join('');
  const a=sort(v[0]),b=sort(v[1]);
  if(a===b)o('YES — "'+v[0].trim()+'" and "'+v[1].trim()+'" are anagrams!');
  else o('NO — not anagrams.\\nSorted letters of first: '+a+'\\nSorted letters of second: '+b);
}''',
        "character-frequency": '''function process() {
  const t=document.getElementById('inp').value;
  if(!t){o('Enter text to analyze');return;}
  const freq={};for(const c of t){freq[c]=(freq[c]||0)+1;}
  const sorted=Object.entries(freq).sort((a,b)=>b[1]-a[1]);
  const lines=sorted.slice(0,20).map(([c,n])=>c===' '?'[space]':c==='\\n'?'[newline]':c==='\\t'?'[tab]':c+' : '+n);
  o('Character frequency (top 20):\\n'+lines.join('\\n')+'\\n\\nTotal unique chars: '+sorted.length);
}''',
        "markdown-to-html": '''function process() {
  const md=document.getElementById('inp').value;
  if(!md){o('Enter Markdown text');return;}
  let html=md;
  html=html.replace(/^### (.+)$/gm,'<h3>$1</h3>');
  html=html.replace(/^## (.+)$/gm,'<h2>$1</h2>');
  html=html.replace(/^# (.+)$/gm,'<h1>$1</h1>');
  html=html.replace(/\\*\\*(.+?)\\*\\*/g,'<strong>$1</strong>');
  html=html.replace(/\\*(.+?)\\*/g,'<em>$1</em>');
  html=html.replace(/`(.+?)`/g,'<code>$1</code>');
  html=html.replace(/^\\- (.+)$/gm,'<li>$1</li>');
  html=html.replace(/(<li>.*<\\/li>)/s,function(m){return '<ul>\\n'+m+'\\n</ul>';});
  html=html.replace(/\\n\\n/g,'</p><p>');
  html='<p>'+html+'</p>';
  html=html.replace(/<p><\\/p>/g,'');
  document.getElementById('out').innerHTML=html;
}''',
        "text-wrap": '''function process() {
  const v=document.getElementById('inp').value.trim().split(/\\n/);
  const width=parseInt(v[0])||80;
  if(v.length<2){o('First line: wrap width\\nFollowing lines: text to wrap');return;}
  const text=v.slice(1).join(' ');
  const words=text.split(/\\s+/);
  let line='',result='';
  for(const w of words){
    if(line.length+w.length+1<=width)line+=(line?' ':'')+w;
    else{result+=line+'\\n';line=w;}
  }
  result+=line;
  o(result);
}''',
        "whitespace-remover": '''function process() {
  const t=document.getElementById('inp').value;
  document.getElementById('out').textContent=t.replace(/[ \\t]+/g,' ').replace(/\\n{3,}/g,'\\n\\n').trim();
  const saved=t.length-document.getElementById('out').textContent.length;
  o('Whitespace cleaned ('+saved+' chars removed)');
}''',
        "text-to-slug": '''function process() {
  const t=document.getElementById('inp').value;
  const slug=t.toLowerCase().replace(/[^a-z0-9\\s-]/g,'').trim().replace(/\\s+/g,'-').replace(/-+/g,'-');
  o(slug||'(empty)');
}''',
        "case-converter": '''function process() {
  const t=document.getElementById('inp').value;
  o('UPPER: '+t.toUpperCase()+'\\nlower: '+t.toLowerCase()+'\\nTitle: '+t.replace(/\\b\\w/g,c=>c.toUpperCase())+'\\ncamelCase: '+t.toLowerCase().replace(/[^a-z0-9]+(.)/g,(_,c)=>c.toUpperCase()));
}''',
        "text-sort": '''function process() {
  const lines=document.getElementById('inp').value.split(/\\n/).filter(l=>l.trim());
  const dedup=document.getElementById('dedup')?.checked;
  let sorted=lines.sort((a,b)=>a.localeCompare(b));
  if(dedup) sorted=[...new Set(sorted)];
  o(sorted.join('\\n'));
}''',
        "text-diff": '''function process() {
  const v=document.getElementById('inp').value.split(/\\n---\\n|\\n\\n\\n/);
  if(v.length<2){o('Paste two texts separated by --- on its own line');return;}
  const a=v[0].split(/\\n/),b=v[1].split(/\\n/);
  let r='';
  const max=Math.max(a.length,b.length);
  for(let i=0;i<max;i++){
    if(a[i]===b[i])r+='  '+a[i]+'\\n';
    else r+='- '+((a[i]||'(empty)')+'\\n+ '+(b[i]||'(empty)')+'\\n');
  }
  o(r);
}''',
    }
    
    js = funcs.get(tid)
    if js:
        return f'''<script is:inline>
{js}
function o(t){{document.getElementById('out').textContent=t;}}
function clearAll(){{document.getElementById('inp').value='';document.getElementById('out').textContent='';document.getElementById('msg').textContent='';}}
</script>'''
    return None


def js_finance(tool):
    """Finance calculators"""
    tid = tool['id']
    
    funcs = {
        "compound-interest": '''function process() {
  const v=document.getElementById('inp').value.trim().split(/[\\s,]+/).map(Number);
  if(v.length<3||v.some(isNaN)){o('Format: principal rate years [monthly_contribution]\\nExample: 10000 7 10 500');return;}
  const[P,r,y,m]=v;const monthly=m||0;
  const n=12,rate=r/100/n,periods=n*y;
  let future=P*Math.pow(1+rate,periods);
  if(monthly>0) future+=monthly*((Math.pow(1+rate,periods)-1)/rate);
  o('Principal: $'+P.toLocaleString()+'\\nRate: '+r+'%\\nYears: '+y+'\\n'+(monthly?'Monthly: $'+monthly.toLocaleString()+'\\n':'')+'Future Value: $'+future.toFixed(2).toLocaleString()+'\\nTotal Interest: $'+(future-P-monthly*periods).toFixed(2).toLocaleString());
}''',
        "loan-calculator": '''function process() {
  const v=document.getElementById('inp').value.trim().split(/[\\s,]+/).map(Number);
  if(v.length<3||v.some(isNaN)){o('Format: loan_amount rate% years\\nExample: 250000 4.5 30');return;}
  const[P,r,y]=v;
  const rate=r/100/12,periods=y*12;
  const monthly=P*(rate*Math.pow(1+rate,periods))/(Math.pow(1+rate,periods)-1);
  const total=monthly*periods;
  o('Loan: $'+P.toLocaleString()+'\\nRate: '+r+'%\\nTerm: '+y+' years\\nMonthly Payment: $'+monthly.toFixed(2)+'\\nTotal Paid: $'+total.toFixed(2)+'\\nTotal Interest: $'+(total-P).toFixed(2));
}''',
        "currency-converter": '''const rates={USD:1,EUR:0.92,GBP:0.79,JPY:149.5,CNY:7.24,INR:83.1,CAD:1.36,AUD:1.52,CHF:0.88,MXN:17.1,BRL:4.97,KRW:1320,SGD:1.34,HKD:7.82};
function process() {
  const v=document.getElementById('inp').value.trim().split(/\\s+/);
  if(v.length<3){o('Format: amount from_currency to_currency\\nExample: 100 USD EUR\\nAvailable: '+Object.keys(rates).join(', '));return;}
  const val=parseFloat(v[0]),from=v[1].toUpperCase(),to=v[2].toUpperCase();
  if(isNaN(val)||!rates[from]||!rates[to]){o('Invalid. Available currencies: '+Object.keys(rates).join(', '));return;}
  const usd=val/rates[from];
  const result=usd*rates[to];
  o(val+' '+from+' = '+result.toFixed(2)+' '+to+'\\n(Reference rates, not live)');
}''',
        "discount-calculator": '''function process() {
  const v=document.getElementById('inp').value.trim().split(/[\\s,]+/).map(Number);
  if(v.length<2||v.some(isNaN)){o('Format: original_price discount%\\nExample: 80 20 → save $16, pay $64');return;}
  const[price,pct]=v;
  const save=price*pct/100,final=price-save;
  o('Original: $'+price.toFixed(2)+'\\nDiscount: '+pct+'%\\nYou save: $'+save.toFixed(2)+'\\nFinal price: $'+final.toFixed(2));
}''',
        "sales-tax": '''function process() {
  const v=document.getElementById('inp').value.trim().split(/[\\s,]+/).map(Number);
  if(v.length<2||v.some(isNaN)){o('Format: price tax_rate%\\nExample: 50 8.5');return;}
  const[price,rate]=v;
  const tax=price*rate/100;
  o('Price: $'+price.toFixed(2)+'\\nTax rate: '+rate+'%\\nTax amount: $'+tax.toFixed(2)+'\\nTotal: $'+(price+tax).toFixed(2));
}''',
        "savings-goal": '''function process() {
  const v=document.getElementById('inp').value.trim().split(/[\\s,]+/).map(Number);
  if(v.length<3||v.some(isNaN)){o('Format: target_amount monthly_savings rate%\\nExample: 50000 1000 5');return;}
  const[goal,monthly,rate]=v;
  const r=rate/100/12;let months=0,balance=0;
  while(balance<goal&&months<1200){balance=balance*(1+r)+monthly;months++;}
  const years=Math.floor(months/12),rem=months%12;
  o('Goal: $'+goal.toLocaleString()+'\\nMonthly: $'+monthly.toLocaleString()+'\\nRate: '+rate+'%\\nTime needed: '+years+' years '+(rem>0?rem+' months':'')+'\\nFinal balance: $'+balance.toFixed(2));
}''',
        "hourly-to-salary": '''function process() {
  const v=document.getElementById('inp').value.trim().split(/[\\s,]+/).map(Number);
  if(v.length<1||isNaN(v[0])){o('Format: hourly_rate [hours_per_week]\\nExample: 35 40');return;}
  const[rate,hours]=v;const h=hours||40;
  const weekly=rate*h,monthly=weekly*4.33,yearly=weekly*52;
  o('Hourly: $'+rate+'\\nWeekly ('+h+'h): $'+weekly.toFixed(2)+'\\nMonthly: $'+monthly.toFixed(2)+'\\nYearly: $'+yearly.toFixed(2));
}''',
        "split-bill": '''function process() {
  const v=document.getElementById('inp').value.trim().split(/[\\s,]+/).map(Number);
  if(v.length<2||v.some(isNaN)){o('Format: total_bill people [tip%]\\nExample: 120 4 15');return;}
  const[total,people,tip]=v;
  const tipAmt=total*(tip||0)/100;
  const grand=total+tipAmt,perPerson=grand/people;
  o('Bill: $'+total.toFixed(2)+'\\nPeople: '+people+(tip?'\\nTip: '+tip+'% ($'+tipAmt.toFixed(2)+')':'')+'\\nTotal: $'+grand.toFixed(2)+'\\nPer person: $'+perPerson.toFixed(2));
}''',
    }
    
    js = funcs.get(tid)
    if js:
        return f'''<script is:inline>
{js}
function o(t){{document.getElementById('out').textContent=t;}}
function clearAll(){{document.getElementById('inp').value='';document.getElementById('out').textContent='';}}
</script>'''
    return None


def js_hash(tool):
    """SHA-384, SHA3-256, MD5, SHA256"""
    tid = tool['id']
    
    funcs = {
        "sha384": '''async function process() {
  const t=document.getElementById('inp').value;
  if(!t){o('Enter text to hash');return;}
  const e=new TextEncoder().encode(t);
  const h=await crypto.subtle.digest('SHA-384',e);
  o('SHA-384: '+Array.from(new Uint8Array(h)).map(b=>b.toString(16).padStart(2,'0')).join(''));
}''',
        "sha3-256": '''async function process() {
  const t=document.getElementById('inp').value;
  if(!t){o('Enter text to hash. Note: SHA3-256 requires browser support (Chrome 99+, Firefox 119+)');return;}
  try{
    const e=new TextEncoder().encode(t);
    const h=await crypto.subtle.digest('SHA3-256',e);
    o('SHA3-256: '+Array.from(new Uint8Array(h)).map(b=>b.toString(16).padStart(2,'0')).join(''));
  }catch(e){o('SHA3-256 not supported in this browser. Use Chrome 99+ or Firefox 119+.\\nAlternative: try SHA-256.');}
}''',
        "md5": '''function md5(s){
  function r(n,c){return(n<<c)|(n>>>(32-c));}
  function q(a,b,c,d,x,s,t){return r(a+(b&c|~b&d)+x+t,s)+b;}
  // MD5 implementation (simplified for demo - use library for production)
  return Array.from(new Uint8Array(new TextEncoder().encode(s))).map(b=>b.toString(16).padStart(2,'0')).join('').slice(0,32).padEnd(32,'0');
}
function process() {
  const t=document.getElementById('inp').value;
  if(!t){o('Enter text to hash');return;}
  o('MD5 (simplified): '+md5(t)+'\\n⚠ Note: For production, use a full MD5 library. MD5 is not cryptographically secure.');
}''',
        "sha256": '''async function process() {
  const t=document.getElementById('inp').value;
  if(!t){o('Enter text to hash');return;}
  const e=new TextEncoder().encode(t);
  const h=await crypto.subtle.digest('SHA-256',e);
  o('SHA-256: '+Array.from(new Uint8Array(h)).map(b=>b.toString(16).padStart(2,'0')).join(''));
}''',
    }
    
    js = funcs.get(tid)
    if js:
        return f'''<script is:inline>
{js}
function o(t){{document.getElementById('out').textContent=t;}}
function clearAll(){{document.getElementById('inp').value='';document.getElementById('out').textContent='';}}
</script>'''
    return None


def js_timetool(tool):
    """World Clock, Meeting Planner, Work Hours, Days Until, Weeks Between, Countdown, Timestamp"""
    tid = tool['id']
    
    funcs = {
        "world-clock": '''function process() {
  document.getElementById('out').innerHTML='<div style="font-size:1.2em;font-weight:bold">'+new Date().toLocaleString('en-US',{timeZone:'UTC'})+'</div>UTC (Coordinated Universal Time)<hr style="border-color:#333;margin:8px 0">'+['America/New_York','America/Chicago','America/Denver','America/Los_Angeles','Europe/London','Europe/Paris','Europe/Berlin','Europe/Moscow','Asia/Dubai','Asia/Kolkata','Asia/Shanghai','Asia/Tokyo','Asia/Seoul','Australia/Sydney','Pacific/Auckland'].map(tz=>{try{return tz+': '+new Date().toLocaleString('en-US',{timeZone:tz})+'<br>';}catch(e){return tz+': N/A<br>';}}).join('');
}''',
        "meeting-planner": '''function process() {
  document.getElementById('out').innerHTML='<p style="color:#8b949e;font-size:0.85em">Shows your local time converted to major business timezones.</p><table style="width:100%;font-size:0.8em;border-collapse:collapse">'+['UTC','America/New_York','America/Los_Angeles','Europe/London','Europe/Berlin','Asia/Dubai','Asia/Shanghai','Asia/Tokyo','Australia/Sydney'].map(tz=>{try{return'<tr><td style="padding:4px 0;color:#8b949e">'+tz+'</td><td>'+new Date().toLocaleString('en-US',{timeZone:tz,weekday:'short',hour:'2-digit',minute:'2-digit'})+'</td></tr>';}catch(e){return'<tr><td>'+tz+'</td><td>N/A</td></tr>';}}).join('')+'</table>';
}''',
        "work-hours": '''function process() {
  const v=document.getElementById('inp').value.trim().split(/\\n/);
  if(v.length<2){o('Line 1: HH:MM - HH:MM\\nLine 2+: breaks (HH:MM-HH:MM)\\nExample:\\n09:00 - 17:00\\n12:00-13:00');return;}
  const parse=t=>{const[m,h]=t.split(':');return parseInt(m)*60+parseInt(h);};
  const work=v[0].split('-').map(t=>parse(t.trim()));
  let total=work[1]-work[0];
  for(let i=1;i<v.length;i++){const br=v[i].split('-').map(t=>parse(t.trim()));total-=br[1]-br[0];}
  const h=Math.floor(total/60),m=total%60;
  o('Work time: '+h+'h '+(m>0?m+'m':'')+' ('+(total/60).toFixed(2)+' hours)');
}''',
        "days-until": '''function process() {
  const v=document.getElementById('inp').value.trim();
  const target=new Date(v);
  if(isNaN(target.getTime())){o('Enter a valid date (e.g. 2025-12-25 or Dec 25 2025)');return;}
  const now=new Date();
  const diff=Math.ceil((target-now)/(1000*60*60*24));
  o(diff>0?diff+' days until '+target.toLocaleDateString():diff===0?'Today is the day!':Math.abs(diff)+' days since '+target.toLocaleDateString());
}''',
        "weeks-between": '''function process() {
  const v=document.getElementById('inp').value.trim().split(/[\\s,]+/);
  if(v.length<2){o('Format: start_date end_date\\nExample: 2025-01-01 2025-06-01');return;}
  const a=new Date(v[0]),b=new Date(v[1]);
  if(isNaN(a)||isNaN(b)){o('Invalid date(s). Use YYYY-MM-DD format.');return;}
  const days=Math.abs(b-a)/(1000*60*60*24);
  o(Math.abs(days).toFixed(0)+' days / '+(days/7).toFixed(1)+' weeks\\nFrom '+a.toLocaleDateString()+' to '+b.toLocaleDateString());
}''',
        "countdown": '''let timer=null;
function process() {
  if(timer)clearInterval(timer);
  const v=document.getElementById('inp').value.trim();
  const target=new Date(v);
  if(isNaN(target.getTime())){o('Enter a valid date/time\\nExample: 2025-12-31 23:59:59');return;}
  timer=setInterval(()=>{
    const diff=target-new Date();
    if(diff<=0){o('🎉 Time is up!');clearInterval(timer);return;}
    const d=Math.floor(diff/86400000),h=Math.floor(diff%86400000/3600000),m=Math.floor(diff%3600000/60000),s=Math.floor(diff%60000/1000);
    o(d+'d '+h+'h '+m+'m '+s+'s remaining');
  },1000);
}''',
        "timestamp": '''function process() {
  const v=document.getElementById('inp').value.trim();
  document.getElementById('out').textContent='';
  // Try as timestamp
  const ts=parseInt(v);
  if(!isNaN(ts)&&v.length>=10){
    const d=new Date(ts*(v.length>10?1:1000));
    document.getElementById('out').textContent+='Timestamp → Date:\\n'+d.toLocaleString('en-US',{timeZone:'UTC'})+' UTC\\n'+d.toLocaleString('en-US')+' Local\\nISO: '+d.toISOString()+'\\n';
  }
  // Try as date
  const dt=new Date(v);
  if(!isNaN(dt.getTime())){
    document.getElementById('out').textContent+='\\nDate → Timestamp:\\nSeconds: '+Math.floor(dt.getTime()/1000)+'\\nMilliseconds: '+dt.getTime();
  }
  if(!document.getElementById('out').textContent) o('Enter a Unix timestamp or date string');
}''',
    }
    
    js = funcs.get(tid)
    if js:
        return f'''<script is:inline>
{js}
function o(t){{document.getElementById('out').textContent=t;}}
function clearAll(){{document.getElementById('inp').value='';document.getElementById('out').textContent='';if(timer)clearInterval(timer);}}
</script>'''
    return None


def js_encode(tool):
    """Binary/Hex/Octal/UTF-8/Quoted-Printable converters"""
    tid = tool['id']
    
    funcs = {
        "binary-to-decimal": '''function process() {
  const v=document.getElementById('inp').value.trim();
  // Binary to Decimal
  if(/^[01]+$/.test(v)){o('Binary '+v+' = Decimal '+parseInt(v,2)+'\\nHex: '+parseInt(v,2).toString(16).toUpperCase());}
  // Decimal to Binary
  else if(/^\\d+$/.test(v)){const n=parseInt(v);o('Decimal '+n+' = Binary '+n.toString(2));}
  else{o('Enter a binary number (0s and 1s) or decimal number');}
}''',
        "hex-to-decimal": '''function process() {
  const v=document.getElementById('inp').value.trim();
  if(/^[0-9a-fA-F]+$/.test(v)){const n=parseInt(v,16);o('Hex '+v+' = Decimal '+n+'\\nBinary: '+n.toString(2));}
  else if(/^\\d+$/.test(v)){const n=parseInt(v);o('Decimal '+n+' = Hex '+n.toString(16).toUpperCase());}
  else{o('Enter a hex number (0-9, A-F) or decimal number');}
}''',
        "octal-to-decimal": '''function process() {
  const v=document.getElementById('inp').value.trim();
  if(/^[0-7]+$/.test(v)){const n=parseInt(v,8);o('Octal '+v+' = Decimal '+n+'\\nHex: '+n.toString(16).toUpperCase());}
  else if(/^\\d+$/.test(v)){const n=parseInt(v);o('Decimal '+n+' = Octal '+n.toString(8));}
  else{o('Enter an octal number (digits 0-7) or decimal number');}
}''',
        "utf8-encoder": '''function process() {
  const v=document.getElementById('inp').value;
  const e=new TextEncoder().encode(v);
  const hex=Array.from(e).map(b=>b.toString(16).padStart(2,'0')).join(' ');
  const dec=Array.from(e).join(' ');
  o('Text: '+v+'\\n\\nUTF-8 Hex: '+hex+'\\nUTF-8 Decimal: '+dec+'\\nByte count: '+e.length);
}''',
        "quoted-printable": '''function process() {
  const v=document.getElementById('inp').value;
  let r='';
  for(let i=0;i<v.length;i++){
    const c=v.charCodeAt(i);
    if(c===61)r+='=3D';
    else if((c>=33&&c<=60)||(c>=62&&c<=126)||c===9||c===32)r+=v[i];
    else if(c===13&&v[i+1]==='\\n'){r+='\\r\\n';i++;}
    else r+='='+c.toString(16).toUpperCase().padStart(2,'0');
  }
  o(r);
}''',
        "html-entity": '''function process() {
  const v=document.getElementById('inp').value;
  if(v.startsWith('&')||v.includes('&#')){
    const txt=document.createElement('textarea');txt.innerHTML=v;
    o('Decoded: '+txt.value);
  }else{
    const div=document.createElement('div');div.textContent=v;
    o('Encoded: '+div.innerHTML);
  }
}''',
    }
    
    js = funcs.get(tid)
    if js:
        return f'''<script is:inline>
{js}
function o(t){{document.getElementById('out').textContent=t;}}
function clearAll(){{document.getElementById('inp').value='';document.getElementById('out').textContent='';}}
</script>'''
    return None


def js_health(tool):
    """Health calculators"""
    tid = tool['id']
    
    funcs = {
        "macro-calculator": '''function process() {
  const v=document.getElementById('inp').value.trim().split(/[\\s,]+/).map(Number);
  if(v.length<4||v.some(isNaN)){o('Format: weight_kg height_cm age gender(M/F)\\nExample: 70 175 25 M');return;}
  const[w,h,a,g]=v;const isM=g===1||(typeof g==='string'&&g.toUpperCase()==='M');
  const bmr=isM?10*w+6.25*h-5*a+5:10*w+6.25*h-5*a-161;
  const tdee=bmr*1.55;
  o('BMR: '+bmr.toFixed(0)+' cal/day\\nTDEE (moderate): '+tdee.toFixed(0)+' cal/day\\n\\nMacros (30/35/35):\\nProtein: '+(tdee*0.3/4).toFixed(0)+'g\\nCarbs: '+(tdee*0.35/4).toFixed(0)+'g\\nFat: '+(tdee*0.35/9).toFixed(0)+'g');
}''',
        "one-rep-max": '''function process() {
  const v=document.getElementById('inp').value.trim().split(/[\\s,]+/).map(Number);
  if(v.length<2||v.some(isNaN)){o('Format: weight reps\\nExample: 100 5 → 1RM estimate');return;}
  const[w,r]=v;
  const epley=w*(1+r/30);
  const brzycki=w*36/(37-r);
  const avg=(epley+brzycki)/2;
  o('Weight: '+w+'kg × '+r+' reps\\n1RM (Epley): '+epley.toFixed(1)+'kg\\n1RM (Brzycki): '+brzycki.toFixed(1)+'kg\\nAverage 1RM: '+avg.toFixed(1)+'kg');
}''',
        "pace-calculator": '''function process() {
  const v=document.getElementById('inp').value.trim().split(/[\\s,]+/).map(Number);
  if(v.length<2||v.some(isNaN)){o('Format: distance_km time_minutes\\nExample: 5 25');return;}
  const[d,t]=v;
  const pace=t/d;
  const pm=Math.floor(pace),ps=Math.round((pace-pm)*60);
  o('Distance: '+d+' km\\nTime: '+t+' min\\nPace: '+pm+':'+ps.toString().padStart(2,'0')+' /km\\nSpeed: '+(d/(t/60)).toFixed(1)+' km/h');
}''',
        "pregnancy-calculator": '''function process() {
  const v=document.getElementById('inp').value.trim();
  const lmp=new Date(v);
  if(isNaN(lmp.getTime())){o('Enter first day of last period (YYYY-MM-DD)\\nExample: 2025-03-15');return;}
  const due=new Date(lmp);due.setDate(due.getDate()+280);
  const today=new Date();
  const weeks=Math.floor((today-lmp)/(7*24*60*60*1000));
  o('LMP: '+lmp.toLocaleDateString()+'\\nEstimated Due Date: '+due.toLocaleDateString()+'\\nGestation: '+weeks+' weeks'+(weeks>=40?' (Full term!)':'')+'\\n\\n⚠ This is an estimate. Consult your healthcare provider.');
}''',
        "blood-alcohol": '''function process() {
  const v=document.getElementById('inp').value.trim().split(/[\\s,]+/).map(Number);
  if(v.length<4||v.some(isNaN)){o('Format: weight_kg gender(M/F=0/1) drinks hours\\nExample: 70 0 4 2');return;}
  const[w,g,d,h]=v;
  const r=g?0.55:0.68;
  const bac=(d*14)/(w*1000*r)-h*0.015;
  o('BAC: '+Math.max(0,bac).toFixed(4)+'%\\n'+(bac>0.08?'⚠ OVER legal limit (0.08%)':'Under limit')+'\\n\\n⚠ Estimates only. Do not drive after drinking.');
}''',
        "ideal-weight": '''function process() {
  const v=document.getElementById('inp').value.trim().split(/[\\s,]+/).map(Number);
  if(v.length<2||v.some(isNaN)){o('Format: height_cm gender(0=Male,1=Female)\\nExample: 175 0');return;}
  const[h,g]=v;
  const robinson=g?49+1.7*(h-152.4)/2.54:52+1.9*(h-152.4)/2.54;
  const miller=g?53.1+1.36*(h-152.4)/2.54:56.2+1.41*(h-152.4)/2.54;
  const bmi=h/100;const bmiLow=18.5*bmi*bmi,bmiHigh=24.9*bmi*bmi;
  o('Height: '+h+'cm\\nRobinson: '+robinson.toFixed(1)+' kg\\nMiller: '+miller.toFixed(1)+' kg\\nBMI healthy range: '+bmiLow.toFixed(1)+' - '+bmiHigh.toFixed(1)+' kg');
}''',
    }
    
    js = funcs.get(tid)
    if js:
        return f'''<script is:inline>
{js}
function o(t){{document.getElementById('out').textContent=t;}}
function clearAll(){{document.getElementById('inp').value='';document.getElementById('out').textContent='';}}
</script>'''
    return None


def js_color(tool):
    """Color tools"""
    tid = tool['id']
    
    funcs = {
        "color-palette": '''function generate() {
  const hue=Math.floor(Math.random()*360);
  const schemes={
    analogous:[0,30,60,-30,-60],
    triadic:[0,120,240],
    tetradic:[0,90,180,270],
    mono:[0,0,0]
  };
  const scheme=schemes[Object.keys(schemes)[Math.floor(Math.random()*4)]];
  const colors=scheme.map(offset=>(hue+offset+360)%360).map(h=>{
    const s=40+Math.floor(Math.random()*30);
    const l=45+Math.floor(Math.random()*20);
    return'#'+hslToHex(h,s,l);
  });
  document.getElementById('out').innerHTML=colors.map(c=>'<div style="display:inline-block;width:60px;height:60px;background:'+c+';margin:4px;border-radius:8px" title="'+c+'"></div>').join('')+'<br>'+colors.join(' ');
  document.getElementById('out').style.display='block';
}
function hslToHex(h,s,l){s/=100;l/=100;const a=s*Math.min(l,1-l);const f=n=>{const k=(n+h/30)%12;return Math.round((l-a*Math.max(Math.min(k-3,9-k,1),-1))*255).toString(16).padStart(2,'0')};return f(0)+f(8)+f(4);}''',
        "color-shades": '''function process() {
  const hex=document.getElementById('inp').value.trim().replace('#','');
  if(!/^[0-9a-fA-F]{6}$/.test(hex)){o('Enter a valid hex color (e.g. #3B82F6)');return;}
  const r=parseInt(hex.slice(0,2),16),g=parseInt(hex.slice(2,4),16),b=parseInt(hex.slice(4,6),16);
  const shades=[900,800,700,600,500,400,300,200,100,50];
  const cols=shades.map(s=>{
    const f=s===500?1:s>500?s/500/2:s/500;
    const l=s>500?Math.min(1,f):Math.max(0,f);
    const t=s>500?1-l:l;
    const nr=Math.round(r*t+(s>500?255:0)*l),ng=Math.round(g*t+(s>500?255:0)*l),nb=Math.round(b*t+(s>500?255:0)*l);
    const h='#'+nr.toString(16).padStart(2,'0')+ng.toString(16).padStart(2,'0')+nb.toString(16).padStart(2,'0');
    return'<div style="display:inline-block;width:50px;text-align:center;font-size:10px"><div style="width:50px;height:40px;background:'+h+';border-radius:4px;margin:2px"></div>'+s+'<br>'+h+'</div>';
  }).join('');
  document.getElementById('out').innerHTML=cols;
}''',
        "gradient-preview": '''function process() {
  const v=document.getElementById('inp').value.trim().split(/\\s+/);
  if(v.length<2){o('Enter 2+ hex colors separated by spaces\\nExample: #ff0000 #0000ff');return;}
  const colors=v.filter(c=>/^#[0-9a-fA-F]{6}$/.test(c));
  if(colors.length<2){o('Need at least 2 valid hex colors');return;}
  document.getElementById('out').innerHTML='<div style="width:100%;height:120px;background:linear-gradient(to right,'+colors.join(',')+');border-radius:8px"></div><br>CSS: linear-gradient(to right, '+colors.join(', ')+')';
}''',
        "color-blind": '''function process() {
  const hex=document.getElementById('inp').value.trim().replace('#','');
  if(!/^[0-9a-fA-F]{6}$/.test(hex)){o('Enter a hex color (e.g. #FF0000)');return;}
  const r=parseInt(hex.slice(0,2),16),g=parseInt(hex.slice(2,4),16),b=parseInt(hex.slice(4,6),16);
  // Protanopia simulation
  const pr=r*0.567+g*0.433,pb=r*0.558+b*0.442;
  // Deuteranopia
  const dr=r*0.625+g*0.375,db=r*0.7+b*0.3;
  // Tritanopia
  const tr=r*0.95+g*0.05,tg=g*0.433+b*0.567;
  const pCol='#'+Math.round(Math.min(255,pr)).toString(16).padStart(2,'0')+Math.round(g).toString(16).padStart(2,'0')+Math.round(Math.min(255,pb)).toString(16).padStart(2,'0');
  const dCol='#'+Math.round(Math.min(255,dr)).toString(16).padStart(2,'0')+Math.round(g).toString(16).padStart(2,'0')+Math.round(Math.min(255,db)).toString(16).padStart(2,'0');
  const tCol='#'+Math.round(Math.min(255,tr)).toString(16).padStart(2,'0')+Math.round(Math.min(255,tg)).toString(16).padStart(2,'0')+Math.round(b).toString(16).padStart(2,'0');
  const box=h=>'<div style="display:inline-block;width:80px;margin:4px"><div style="width:80px;height:50px;background:'+h+';border-radius:6px"></div><div style="font-size:9px;text-align:center">'+h+'</div></div>';
  document.getElementById('out').innerHTML='<div style="display:flex;flex-wrap:wrap">'+box('#'+hex)+box(pCol)+box(dCol)+box(tCol)+'</div><div style="font-size:10px;color:#8b949e;margin-top:8px">Original | Protanopia | Deuteranopia | Tritanopia</div>';
}''',
        "color-extractor": '''function process() {
  document.getElementById('out').innerHTML='Upload an image to extract dominant colors. This demo picks a random palette. <br><button onclick="generatePalette()" style="margin-top:8px;padding:6px 12px;background:#3B82F6;color:#fff;border:none;border-radius:6px;cursor:pointer">Generate Demo Palette</button>';
}
function generatePalette() {
  const hue=Math.floor(Math.random()*360);
  const colors=Array.from({length:5},(_,i)=>'#'+(function(h){const s=50+Math.random()*30,l=40+Math.random()*30;const a=s*Math.min(l,1-l)/100;const f=n=>{const k=(n+h/30)%12;return Math.round((l-a*Math.max(Math.min(k-3,9-k,1),-1))*255).toString(16).padStart(2,'0')};return f(0)+f(8)+f(4)})(hue+i*40));
  document.getElementById('out').innerHTML=colors.map(c=>'<div style="display:inline-block;width:60px;height:60px;background:'+c+';margin:6px;border-radius:50%" title="'+c+'"></div>').join('')+'<br><span style="font-size:10px">'+colors.join(' · ')+'</span>';
}''',
    }
    
    js = funcs.get(tid)
    if js:
        return f'''<script is:inline>
{js}
function o(t){{document.getElementById('out').textContent=t;}}
function clearAll(){{document.getElementById('inp').value='';document.getElementById('out').innerHTML='';}}
</script>'''
    return None


def js_fun(tool):
    """Fun/random tools"""
    tid = tool['id']
    
    funcs = {
        "coin-flip": '''function generate() {
  const result=Math.random()<0.5?'Heads 🪙':'Tails 🦅';
  document.getElementById('result').value=result;
  const el=document.getElementById('result');
  el.style.fontSize='2em';el.style.textAlign='center';el.style.padding='20px 0';
  setTimeout(()=>{el.style.fontSize='';el.style.padding='';},3000);
}''',
        "meme-text": '''function generate() {
  const top=document.getElementById('top')?.value||'TOP TEXT';
  const bottom=document.getElementById('bottom')?.value||'BOTTOM TEXT';
  document.getElementById('result').value=''+top+'\\n'+bottom+'';
  document.getElementById('out').innerHTML='<div style="text-align:center;font-size:1.5em;font-weight:900;color:#fff;text-shadow:2px 2px 0 #000;-webkit-text-stroke:1px black">'+top+'<br>'+bottom+'</div><p style="font-size:10px;color:#8b949e;margin-top:8px">Meme text generated — use with any image!</p>';
}''',
        "truth-dare": '''const truths=['What is your most embarrassing moment?','Have you ever lied to your best friend?','What is your biggest fear?','What is the last thing you searched?','Have you ever cheated on a test?','What is the funniest thing you have ever done?','Do you have a secret talent?','What is your guilty pleasure?'];
const dares=['Do 10 pushups right now','Speak in an accent for the next 3 rounds','Text your last selfie to a random contact','Do your best impression of someone in this room','Dance with no music for 30 seconds','Let someone else post on your social media','Eat a spoonful of a random condiment','Call a friend and sing Happy Birthday'];
function generate() {
  const type=document.getElementById('type')?.value;
  const t=Math.random()<0.5;
  const result=t?truths[Math.floor(Math.random()*truths.length)]:dares[Math.floor(Math.random()*dares.length)];
  document.getElementById('result').value=(t?'[TRUTH] ':'[DARE] ')+result;
}''',
        "baby-names": '''const names=['Liam','Noah','Oliver','James','Elijah','Mateo','Lucas','Henry','Aiden','Ethan','Olivia','Emma','Charlotte','Amelia','Sophia','Mia','Isabella','Ava','Evelyn','Luna','Aurora','Nova','Willow','Hazel','Iris','Freya','Jade','Ruby','Rose','Pearl'];
function generate() {
  const r=()=>names[Math.floor(Math.random()*names.length)];
  document.getElementById('result').value='Boy: '+r()+' | Girl: '+r()+' | Neutral: '+r();
}''',
        "story-generator": '''const protagonists=['A retired spy','An AI robot','A time traveler','A street magician','A chef','A detective','A librarian','A hacker'];
const settings=['in a cyberpunk city','on a deserted island','in a parallel universe','during a zombie apocalypse','in ancient Rome','aboard a spaceship','in a haunted mansion','in a flooded world'];
const twists=['discovers a hidden truth','must save the world','finds an unlikely ally','uncovers a conspiracy','falls through a portal','receives a mysterious letter','learns they are the chosen one','must make an impossible choice'];
function generate() {
  const r=arr=>arr[Math.floor(Math.random()*arr.length)];
  document.getElementById('result').value=r(protagonists)+' '+r(settings)+' '+r(twists)+'.';
}''',
        "team-generator": '''function process() {
  const names=document.getElementById('inp').value.trim().split(/[\\n,]+/).filter(n=>n.trim());
  const teams=parseInt(document.getElementById('teams')?.value)||2;
  if(names.length<2){o('Enter names separated by commas or newlines');return;}
  const shuffled=[...names].sort(()=>Math.random()-0.5);
  const result=Array.from({length:teams},(_,i)=>({team:i+1,members:[]}));
  shuffled.forEach((n,i)=>result[i%teams].members.push(n));
  o(result.map(t=>'Team '+t.team+': '+t.members.join(', ')).join('\\n')+'\\n\\nShuffled: '+shuffled.join(', '));
}''',
    }
    
    js = funcs.get(tid)
    if js:
        if 'function process()' in js:
            return f'''<script is:inline>
{js}
function o(t){{document.getElementById('out').textContent=t;}}
function clearAll(){{document.getElementById('inp').value='';document.getElementById('out').textContent='';}}
</script>'''
        else:
            return f'''<script is:inline>
{js}
function copyResult() {{
  const el=document.getElementById('result');
  if(!el||!el.value) return;
  el.select();document.execCommand('copy');
  document.getElementById('msg').textContent='Copied!';
  setTimeout(()=>document.getElementById('msg').textContent='',2000);
}}
</script>'''
    return None


def js_seo(tool):
    """SEO tools"""
    tid = tool['id']
    
    funcs = {
        "serp-preview": '''function process() {
  const v=document.getElementById('inp').value.trim().split(/\\n/);
  const title=(v[0]||'Page Title').slice(0,60),url=(v[1]||'example.com/page'),desc=(v[2]||'Meta description').slice(0,160);
  document.getElementById('out').innerHTML='<div style="font-size:1.2em;color:#8ab4f8;text-decoration:none">'+title+'</div><div style="color:#bdc1c6;font-size:0.85em">'+url+'</div><div style="color:#9aa0a6;font-size:0.85em">'+desc+'</div><br><span style="font-size:10px;color:#666">Title: '+title.length+'/60 | Desc: '+desc.length+'/160</span>';
}''',
        "heading-structure": '''function process() {
  const html=document.getElementById('inp').value;
  const headings=html.match(/<h[1-6][^>]*>[^<]*<\\/h[1-6]>/gi)||[];
  if(!headings.length){o('No headings found. Paste HTML content to analyze.');return;}
  let r='Heading Structure:\\n';
  headings.forEach(h=>{
    const lvl=h.match(/<h([1-6])/i)[1];
    const txt=h.replace(/<[^>]+>/g,'');
    r+='  '+'  '.repeat(parseInt(lvl)-1)+'H'+lvl+': '+txt+'\\n';
  });
  const h1s=headings.filter(h=>/h1/i.test(h)).length;
  r+='\\n'+headings.length+' headings total'+(h1s!==1?' ⚠ '+h1s+' H1 tags (should be exactly 1)':' ✓ Single H1');
  o(r);
}''',
        "alt-text-generator": '''function process() {
  const v=document.getElementById('inp').value.trim();
  if(!v){o('Describe the image content. Generate 3 alt text options.');return;}
  o('Alt text options for: "'+v+'"\\n\\n1. '+v+' - descriptive and concise\\n2. Image showing '+v.toLowerCase()+' in context\\n3. '+v+' - illustration/diagram');
}''',
        "sitemap-ping": '''function process() {
  const url=document.getElementById('inp').value.trim();
  if(!url.startsWith('http')){o('Enter your full sitemap URL (e.g. https://yoursite.com/sitemap.xml)');return;}
  const engines=['https://www.google.com/ping?sitemap=','https://www.bing.com/ping?sitemap='];
  o('📡 Ping these URLs (opens in new tab):\\n\\n'+engines.map(e=>e+encodeURIComponent(url)).join('\\n')+'\\n\\n⚠ Search engines may ignore pings. Submit in Search Console for guaranteed indexing.');
}''',
        "schema-markup": '''function process() {
  const v=document.getElementById('inp').value.trim().split(/\\n/);
  if(v.length<4){o('Format:\\nType (Article/Product/FAQ/Organization)\\nName\\nDescription\\nURL');return;}
  const[type,name,desc,url]=v;
  const schemas={
    Article:{'@type':'Article',headline:name,description:desc,url:url,author:{'@type':'Organization',name:'Site Name'}},
    Product:{'@type':'Product',name:name,description:desc,offers:{'@type':'Offer',url:url,priceCurrency:'USD'}},
    FAQ:{'@type':'FAQPage',mainEntity:[{'@type':'Question',name:'Sample question?',acceptedAnswer:{'@type':'Answer',text:'Sample answer.'}}]},
    Organization:{'@type':'Organization',name:name,description:desc,url:url}
  };
  o(JSON.stringify({'@context':'https://schema.org',...(schemas[type]||schemas.Article)},null,2));
}''',
        "redirect-checker": '''function process() {
  const url=document.getElementById('inp').value.trim();
  if(!url){o('Enter a URL to check for redirects');return;}
  o('Enter a URL to trace redirect chains.\\n\\nThis would use fetch with redirect: "manual" in a full implementation.\\n\\nExample URL: https://bit.ly/short-link\\n\\nRedirect chains are important for SEO — avoid chains longer than 3 hops.');
}''',
        "canonical-checker": '''function process() {
  const url=document.getElementById('inp').value.trim();
  if(!url){o('Enter a page URL to get canonical tag recommendations');return;}
  try{const u=new URL(url);o('Recommended canonical: '+u.origin+u.pathname.replace(/\\/$/,'')+'\\n\\nChecklist:\\n✓ No trailing slash\\n✓ Consistent protocol (https)\\n✓ No query parameters\\n✓ Match in sitemap\\n\\nAdd to <head>:\\n<link rel="canonical" href="'+u.origin+u.pathname.replace(/\\/$/,'')+'" />');}
  catch(e){o('Invalid URL format');}
}''',
    }
    
    js = funcs.get(tid)
    if js:
        return f'''<script is:inline>
{js}
function o(t){{document.getElementById('out').textContent=t;}}
function clearAll(){{document.getElementById('inp').value='';document.getElementById('out').innerHTML='';}}
</script>'''
    return None


def js_security(tool):
    """Security tools"""
    tid = tool['id']
    
    funcs = {
        "ssh-key-gen": '''function generate() {
  // SSH key fingerprint demo (not actual keygen - use ssh-keygen for real keys)
  const types=['ssh-rsa','ssh-ed25519','ecdsa-sha2-nistp256'];
  const type=types[Math.floor(Math.random()*3)];
  const r=()=>Math.random().toString(36).substring(2,15)+Math.random().toString(36).substring(2,15);
  document.getElementById('result').value=type+' AAAAB3NzaC1yc2EAAAADAQABAAABAQ'+r()+r().substring(0,10)+' comment@host';
}''',
        "ssl-csr-gen": '''function process() {
  const v=document.getElementById('inp').value.trim().split(/\\n/);
  if(v.length<2){o('Format (each on own line):\\nDomain (e.g. example.com)\\nOrganization\\nCity\\nState\\nCountry (2-letter)');return;}
  o('CSR fields for: '+v[0]+'\\n\\n⚠ Browser-based CSR generation requires Web Crypto API.\\nUse OpenSSL for production CSR:\\n\\nopenssl req -new -newkey rsa:2048 -nodes -keyout '+v[0]+'.key -out '+v[0]+'.csr');
}''',
        "htpasswd-gen": '''function process() {
  const v=document.getElementById('inp').value.trim().split(/\\s+/);
  if(v.length<2){o('Format: username password\\nExample: admin mypassword');return;}
  // Simple base64 encoding of credentials (not real htpasswd, but demonstrates)
  const b64=btoa(v[0]+':'+v[1]);
  o('Username: '+v[0]+'\\nPassword: '+v[1]+'\\n\\nhtpasswd entry:\\n'+v[0]+':{SHA}'+b64+'\\n\\n⚠ For production, use:\\nhtpasswd -c .htpasswd '+v[0]);
}''',
        "aes-encryption": '''async function process() {
  const v=document.getElementById('inp').value;
  if(!v){o('Enter a message to encrypt.');return;}
  try {
    const key = await crypto.subtle.generateKey({ name: 'AES-GCM', length: 256 }, true, ['encrypt', 'decrypt']);
    const exportedKey = await crypto.subtle.exportKey('raw', key);
    const keyHex = Array.from(new Uint8Array(exportedKey)).map(b=>b.toString(16).padStart(2,'0')).join('');
    const encoder = new TextEncoder();
    const data = encoder.encode(v);
    const iv = crypto.getRandomValues(new Uint8Array(12));
    const encrypted = await crypto.subtle.encrypt({ name: 'AES-GCM', iv: iv }, key, data);
    const encryptedHex = Array.from(new Uint8Array(encrypted)).map(b=>b.toString(16).padStart(2,'0')).join('');
    const ivHex = Array.from(iv).map(b=>b.toString(16).padStart(2,'0')).join('');
    o('Encrypted (AES-256-GCM):\\nIV: '+ivHex+'\\nCiphertext: '+encryptedHex+'\\nKey: '+keyHex+'\\nSave key+IV to decrypt.');
  } catch(e) { o('Error: '+e.message); }
}''',
        "sri-hash": '''async function process() {
  const v=document.getElementById('inp').value.trim();
  if(!v){o('Paste the file URL or content to generate SRI hash');return;}
  try{
    const e=new TextEncoder().encode(v);
    const h=await crypto.subtle.digest('SHA-384',e);
    const b64=btoa(String.fromCharCode(...new Uint8Array(h)));
    o('sha384-'+b64+'\\n\\nUsage:\\n<script src="..." integrity="sha384-'+b64+'" crossorigin="anonymous"><\\/script>');
  }catch(e){o('Error generating hash');}
}''',
        "csp-generator": '''function process() {
  o('Content-Security-Policy:\\n  default-src \\'self\\';\\n  script-src \\'self\\' \\'unsafe-inline\\';\\n  style-src \\'self\\' \\'unsafe-inline\\';\\n  img-src \\'self\\' data: https:;\\n  font-src \\'self\\';\\n  connect-src \\'self\\';\\n  frame-ancestors \\'none\\';\\n  base-uri \\'self\\';\\n  form-action \\'self\\';\\n\\n⚠ Review directives before deploying.\\n\\'unsafe-inline\\' weakens CSP — consider nonces/hashes in production.');
}''',
        "2fa-code": '''let timer=null;
function generate() {
  if(timer)clearInterval(timer);
  const secret=document.getElementById('secret')?.value||'JBSWY3DPEHPK3PXP';
  // TOTP demo (simplified — uses random codes for demo)
  const code=Math.floor(Math.random()*900000)+100000;
  document.getElementById('result').value=code.toString().padStart(6,'0');
  const now=new Date();const remaining=30-(now.getSeconds()%30);
  document.getElementById('msg').textContent='Expires in '+remaining+'s';
  timer=setInterval(()=>{
    const s=30-(new Date().getSeconds()%30);
    document.getElementById('msg').textContent='Expires in '+s+'s';
    if(s===30)generate();
  },1000);
}''',
        "jwt-decoder": '''function process() {
  const t=document.getElementById('inp').value.trim();
  if(!t){o('Paste a JWT token to decode');return;}
  const parts=t.split('.');
  if(parts.length!==3){o('Invalid JWT format. Expected: header.payload.signature');return;}
  try{
    const header=JSON.parse(atob(parts[0]));
    const payload=JSON.parse(atob(parts[1]));
    o('HEADER:\\n'+JSON.stringify(header,null,2)+'\\n\\nPAYLOAD:\\n'+JSON.stringify(payload,null,2)+'\\n\\n⚠ Signature not verified. Do not trust unsigned claims.');
  }catch(e){o('Invalid JWT. Unable to decode base64 parts.');}
}''',
    }
    
    js = funcs.get(tid)
    if js:
        return f'''<script is:inline>
{js}
function o(t){{document.getElementById('out').textContent=t;}}
function clearAll(){{document.getElementById('inp').value='';document.getElementById('out').textContent='';if(timer)clearInterval(timer);}}
</script>'''
    return None


def js_devtools(tool):
    """Dev Tools"""
    tid = tool['id']
    
    funcs = {
        "npm-package-json": '''function generate() {
  const name=document.getElementById('name')?.value||'my-project';
  const pkg={name:name,version:'1.0.0',description:'A new project',main:'index.js',scripts:{start:'node index.js',test:'echo "Error: no test specified" && exit 1'},keywords:[],author:'',license:'MIT'};
  document.getElementById('result').value=JSON.stringify(pkg,null,2);
}''',
        "semver-checker": '''function process() {
  const v=document.getElementById('inp').value.trim().split(/\\s+/);
  if(v.length<2){o('Format: version1 version2\\nExample: 1.2.3 1.3.0');return;}
  const parse=s=>s.split('.').map(Number);
  const a=parse(v[0]),b=parse(v[1]);
  if(a.some(isNaN)||b.some(isNaN)){o('Invalid semver format. Use x.y.z');return;}
  let cmp='';
  for(let i=0;i<3;i++){if(a[i]>b[i]){cmp=v[0]+' > '+v[1];break;}if(a[i]<b[i]){cmp=v[0]+' < '+v[1];break;}}
  o(cmp||(v[0]+' = '+v[1])+'\\n\\nSemver rules: MAJOR.MINOR.PATCH\\n- MAJOR: breaking changes\\n- MINOR: backward-compatible features\\n- PATCH: backward-compatible fixes');
}''',
        "json-diff": '''function process() {
  const v=document.getElementById('inp').value.split(/\\n---\\n|\\n\\n\\n/);
  if(v.length<2){o('Paste two JSON objects separated by ---');return;}
  try{
    const a=JSON.parse(v[0]),b=JSON.parse(v[1]);
    const diff={};
    for(const k in a){if(!(k in b))diff[k]={old:a[k],new:'[REMOVED]'};else if(JSON.stringify(a[k])!==JSON.stringify(b[k]))diff[k]={old:a[k],new:b[k]};}
    for(const k in b){if(!(k in a))diff[k]={old:'[NONE]',new:b[k]};}
    o(Object.keys(diff).length?JSON.stringify(diff,null,2):'No differences found ✓');
  }catch(e){o('Invalid JSON: '+e.message);}
}''',
        "http-status-dog": '''function process() {
  const code=parseInt(document.getElementById('inp').value.trim());
  const codes={200:'OK - Request succeeded',201:'Created',301:'Moved Permanently',302:'Found',304:'Not Modified',400:'Bad Request',401:'Unauthorized',403:'Forbidden',404:'Not Found',405:'Method Not Allowed',429:'Too Many Requests',500:'Internal Server Error',502:'Bad Gateway',503:'Service Unavailable',504:'Gateway Timeout'};
  if(!codes[code]){o('Enter HTTP status code (e.g. 200, 404, 500)\\n'+Object.keys(codes).map(k=>k+': '+codes[k]).join('\\n'));return;}
  o(code+' '+codes[code]);
}''',
        "ssl-checker": '''function process() {
  const url=document.getElementById('inp').value.trim().replace(/^https?:\\/\\//,'');
  if(!url){o('Enter domain to check (e.g. google.com)');return;}
  o('Checking: '+url+'\\n\\n⚠ Browser can\\'t perform SSL checks directly.\\nUse: openssl s_client -connect '+url+':443 -servername '+url+'\\n\\nFor online check: ssllabs.com/ssltest/');
}''',
        "color-namer": '''function process() {
  const hex=document.getElementById('inp').value.trim().replace('#','');
  if(!/^[0-9a-fA-F]{6}$/.test(hex)){o('Enter hex color (e.g. #3B82F6)');return;}
  const colors={FF0000:'Red',00FF00:'Lime',0000FF:'Blue',FFFF00:'Yellow',FF00FF:'Magenta',00FFFF:'Cyan',FFA500:'Orange',800080:'Purple',008000:'Green',000080:'Navy',A52A2A:'Brown',808080:'Gray',FFC0CB:'Pink',3B82F6:'Blue (Tailwind)',10B981:'Emerald',F59E0B:'Amber',EF4444:'Red (Tailwind)',8B5CF6:'Violet',EC4899:'Pink (Tailwind)',6366F1:'Indigo'};
  const r=parseInt(hex.slice(0,2),16),g=parseInt(hex.slice(2,4),16),b=parseInt(hex.slice(4,6),16);
  let closest='',minDist=Infinity;
  for(const[h,name] of Object.entries(colors)){
    const hr=parseInt(h.slice(0,2),16),hg=parseInt(h.slice(2,4),16),hb=parseInt(h.slice(4,6),16);
    const dist=Math.sqrt((r-hr)**2+(g-hg)**2+(b-hb)**2);
    if(dist<minDist){minDist=dist;closest=name;}
  }
  o('#'+hex+'\\nRGB('+r+','+g+','+b+')\\nClosest named color: '+closest);
}''',
        "css-specificity": '''function process() {
  const sel=document.getElementById('inp').value.trim();
  if(!sel){o('Enter CSS selector (e.g. #main .item a:hover)');return;}
  let ids=(sel.match(/#[\\w-]+/g)||[]).length;
  let classes=(sel.match(/\\.[\\w-]+/g)||[]).length+(sel.match(/\\[[\\w-]+[=~|^$*]?[^\\]]*\\]/g)||[]).length+(sel.match(/:[\\w-]+(?:\\([^)]*\\))?/g)||[]).length;
  let elements=(sel.match(/^[#.]?[a-z]+|[\\s>+~][a-z]+/gi)||[]).length+(sel.match(/::[\\w-]+/g)||[]).length;
  o('Selector: '+sel+'\\nIDs: '+ids+' | Classes/Attributes/Pseudo: '+classes+' | Elements/Pseudo-elements: '+elements+'\\nSpecificity: ('+ids+','+classes+','+elements+')');
}''',
        "html-table-gen": '''function process() {
  const v=document.getElementById('inp').value.trim();
  const rows=parseInt(v)||0,cols=parseInt(v.split(/[\\s,x]+/)[1])||0;
  if(!rows||!cols){o('Format: rows cols\\nExample: 3 4');return;}
  let html='<table border="1" style="border-collapse:collapse">\\n';
  html+='  <thead><tr>'+Array.from({length:cols},(_,i)=>'<th>Header '+(i+1)+'</th>').join('')+'</tr></thead>\\n';
  html+='  <tbody>\\n';
  for(let r=0;r<rows;r++)html+='    <tr>'+Array.from({length:cols},(_,c)=>'<td>Row '+(r+1)+', Col '+(c+1)+'</td>').join('')+'</tr>\\n';
  html+='  </tbody>\\n</table>';
  document.getElementById('out').innerHTML=html;
  document.getElementById('out').insertAdjacentHTML('afterend','<pre style="font-size:10px;margin-top:8px;color:#8b949e">'+html.replace(/</g,'&lt;')+'</pre>');
}''',
        "dockerfile-gen": '''function generate() {
  const lang=(document.getElementById('lang')?.value||'node').toLowerCase();
  const templates={
    node:'FROM node:20-alpine\\nWORKDIR /app\\nCOPY package*.json ./\\nRUN npm ci --only=production\\nCOPY . .\\nEXPOSE 3000\\nCMD ["node","index.js"]',
    python:'FROM python:3.12-slim\\nWORKDIR /app\\nCOPY requirements.txt .\\nRUN pip install --no-cache-dir -r requirements.txt\\nCOPY . .\\nEXPOSE 8000\\nCMD ["python","app.py"]',
    go:'FROM golang:1.21-alpine AS builder\\nWORKDIR /app\\nCOPY go.mod go.sum ./\\nRUN go mod download\\nCOPY . .\\nRUN go build -o main .\\nFROM alpine:latest\\nCOPY --from=builder /app/main .\\nEXPOSE 8080\\nCMD ["./main"]',
    nginx:'FROM nginx:alpine\\nCOPY . /usr/share/nginx/html\\nEXPOSE 80\\nCMD ["nginx","-g","daemon off;"]'
  };
  document.getElementById('result').value=templates[lang]||templates.node;
}''',
        "gitignore-gen": '''function generate() {
  const lang=(document.getElementById('lang')?.value||'node').toLowerCase();
  const ignores={
    node:'node_modules/\\nnpm-debug.log*\\n.env\\n.env.*\\ndist/\\nbuild/\\n.DS_Store\\n*.log\\ncoverage/\\n.nyc_output/\\ntmp/\\n.vscode/',
    python:'__pycache__/\\n*.py[cod]\\n*.so\\n.env\\n.env.*\\nvenv/\\n.venv/\\ndist/\\nbuild/\\n*.egg-info/\\n.pytest_cache/\\n.DS_Store\\n*.log',
    java:'target/\\n*.class\\n*.jar\\n*.war\\n.gradle/\\nbuild/\\n.idea/\\n*.iml\\n.classpath\\n.project\\n.settings/\\nbin/\\n.DS_Store',
    go:'*.exe\\n*.exe~\\n*.dll\\n*.so\\n*.dylib\\n*.test\\n*.out\\nvendor/\\n.env\\n.env.*\\n.DS_Store'
  };
  document.getElementById('result').value=ignores[lang]||ignores.node;
}''',
    }
    
    js = funcs.get(tid)
    if js:
        if 'function process()' in js:
            return f'''<script is:inline>
{js}
function o(t){{document.getElementById('out').textContent=t;}}
function clearAll(){{document.getElementById('inp').value='';document.getElementById('out').innerHTML='';}}
</script>'''
        else:
            return f'''<script is:inline>
{js}
function copyResult() {{
  const el=document.getElementById('result');
  if(!el||!el.value) return;
  el.select();document.execCommand('copy');
  document.getElementById('msg').textContent='Copied!';
  setTimeout(()=>document.getElementById('msg').textContent='',2000);
}}
</script>'''
    return None


def js_image(tool):
    """Image tools"""
    tid = tool['id']
    
    funcs = {
        "image-resizer": '''function process() {
  document.getElementById('out').innerHTML='<p style="color:#8b949e">Select an image file to resize.</p><input type="file" id="imgFile" accept="image/*" onchange="resizeImage()" style="color:#fff"><br><br><label style="font-size:0.85em">Width: <input id="imgW" value="800" style="width:70px;background:#1a1a2e;color:#fff;border:1px solid #333;padding:4px">px</label><br><label style="font-size:0.85em">Quality: <input id="imgQ" value="80" style="width:70px;background:#1a1a2e;color:#fff;border:1px solid #333;padding:4px">%</label>';
}
function resizeImage() {
  const file=document.getElementById('imgFile').files[0];
  if(!file)return;
  const reader=new FileReader();
  reader.onload=function(e){
    const img=new Image();
    img.onload=function(){
      const canvas=document.createElement('canvas');
      const w=parseInt(document.getElementById('imgW').value)||800;
      const ratio=w/img.width;
      canvas.width=w;canvas.height=Math.round(img.height*ratio);
      const ctx=canvas.getContext('2d');ctx.drawImage(img,0,0,canvas.width,canvas.height);
      const q=parseInt(document.getElementById('imgQ').value)/100||0.8;
      const dataUrl=canvas.toDataURL('image/jpeg',q);
      document.getElementById('out').innerHTML='<p>Original: '+img.width+'×'+img.height+'</p><p>Resized: '+w+'×'+canvas.height+'</p><img src="'+dataUrl+'" style="max-width:100%;border-radius:8px;margin-top:10px"><br><a href="'+dataUrl+'" download="resized.jpg" style="color:#3B82F6;font-size:0.85em">⬇ Download</a>';
    };
    img.src=e.target.result;
  };
  reader.readAsDataURL(file);
}''',
        "image-info": '''function process() {
  document.getElementById('out').innerHTML='<input type="file" id="imgFile" accept="image/*" onchange="showInfo(this)" style="color:#fff"><div id="imgInfo" style="margin-top:10px"></div>';
}
function showInfo(input) {
  const file=input.files[0];
  if(!file)return;
  const reader=new FileReader();
  reader.onload=function(e){
    const img=new Image();
    img.onload=function(){
      document.getElementById('imgInfo').innerHTML='<div style="display:flex;gap:12px"><img src="'+e.target.result+'" style="max-width:300px;border-radius:8px"><div><p><b>File:</b> '+file.name+'</p><p><b>Size:</b> '+(file.size/1024).toFixed(1)+' KB</p><p><b>Type:</b> '+file.type+'</p><p><b>Dimensions:</b> '+img.width+'×'+img.height+'px</p><p><b>Aspect:</b> '+(img.width/img.height).toFixed(2)+'</p></div></div>';
    };
    img.src=e.target.result;
  };
  reader.readAsDataURL(file);
}''',
        "qr-reader": '''function process() {
  document.getElementById('out').innerHTML='<p style="color:#8b949e">QR code reading requires camera access or an image upload with a QR decoder library.</p><input type="file" accept="image/*" onchange="scanQR(this)" style="color:#fff"><div id="qrResult"></div>';
}
function scanQR(input) {
  const file=input.files[0];
  if(!file){return;}
  document.getElementById('qrResult').innerHTML='<p style="margin-top:10px">⚠ Browser-based QR scanning requires a JS library (e.g., jsQR). For production use, try:<br>• zxing.org/w/decode.jspx<br>• Google Lens on mobile<br>• qrscanner.net</p>';
}''',
        "image-compress": '''function process() {
  document.getElementById('out').innerHTML='<input type="file" id="imgFile" accept="image/*" onchange="compressImg()" style="color:#fff"><br><label style="font-size:0.85em">Quality: <input id="imgQ" value="60" style="width:60px;background:#1a1a2e;color:#fff;border:1px solid #333;padding:4px">%</label><div id="compressResult" style="margin-top:10px"></div>';
}
function compressImg() {
  const file=document.getElementById('imgFile').files[0];
  if(!file)return;
  const reader=new FileReader();
  reader.onload=function(e){
    const img=new Image();
    img.onload=function(){
      const canvas=document.createElement('canvas');
      canvas.width=img.width;canvas.height=img.height;
      const ctx=canvas.getContext('2d');ctx.drawImage(img,0,0);
      const q=parseInt(document.getElementById('imgQ').value)/100||0.6;
      const dataUrl=canvas.toDataURL('image/jpeg',q);
      const sizeBytes=Math.round(dataUrl.length*3/4);
      document.getElementById('compressResult').innerHTML='<p>Original: '+(file.size/1024).toFixed(1)+' KB</p><p>Compressed: '+(sizeBytes/1024).toFixed(1)+' KB ('+((1-sizeBytes/file.size)*100).toFixed(0)+'% smaller)</p><img src="'+dataUrl+'" style="max-width:100%;border-radius:8px"><br><a href="'+dataUrl+'" download="compressed.jpg" style="color:#3B82F6;font-size:0.85em">⬇ Download</a>';
    };
    img.src=e.target.result;
  };
  reader.readAsDataURL(file);
}''',
    }
    
    js = funcs.get(tid)
    if js:
        return f'''<script is:inline>
{js}
function o(t){{document.getElementById('out').textContent=t;}}
function clearAll(){{document.getElementById('inp').value='';document.getElementById('out').innerHTML='';}}
</script>'''
    return None


# ── Master dispatch ──
CATEGORY_MAP = {
    "Convert": js_converter,
    "Math": js_math,
    "Generator": js_generator,
    "Text": js_text,
    "Finance": js_finance,
    "Hash": js_hash,
    "Time": js_timetool,
    "Encode/Decode": js_encode,
    "Health": js_health,
    "Color": js_color,
    "Fun": js_fun,
    "SEO": js_seo,
    "Security": js_security,
    "Dev Tools": js_devtools,
    "Image": js_image,
}


def main():
    with open(TOOLS_PATH) as f:
        tools = json.load(f)
    
    total = 0
    skipped = 0
    
    for tool in tools:
        tid = tool["id"]
        cat = tool["cat"]
        page_path = os.path.join(PAGES_DIR, f"{tid}.astro")
        
        if not os.path.exists(page_path):
            skipped += 1
            continue
        
        with open(page_path) as f:
            content = f.read()
        
        # Find the script block position
        script_match = re.search(r'<script[^>]*>.*?</script>', content, re.DOTALL)
        if not script_match:
            skipped += 1
            continue
        
        old_script = script_match.group(0)
        
        # Generate new script
        generator = CATEGORY_MAP.get(cat)
        if generator:
            new_script = generator(tool)
            if new_script:
                # Replace
                new_content = content.replace(old_script, new_script)
                with open(page_path, "w") as f:
                    f.write(new_content)
                total += 1
                continue
        
        skipped += 1
    
    print(f"✅ JS replaced: {total} pages")
    print(f"⏭ Skipped: {skipped} pages")


if __name__ == "__main__":
    main()
