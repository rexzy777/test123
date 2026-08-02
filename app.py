import http.server
import json
import re
import zipfile
import io
import os
import tempfile
import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

PORT = 9999
PROXY_URL = "http://np_cdub79ml1s:cvVvAgD3K6PeGcl5@global.nodeproxies.xyz:8080"

API_URL = "https://ios.prod.ftl.netflix.com/iosui/user/15.48"
QUERY_PARAMS = {
    "appVersion": "15.48.1",
    "config": '{"gamesInTrailersEnabled":"false","isTrailersEvidenceEnabled":"false","cdsMyListSortEnabled":"true","kidsBillboardEnabled":"true","addHorizontalBoxArtToVideoSummariesEnabled":"false","skOverlayTestEnabled":"false","homeFeedTestTVMovieListsEnabled":"false","baselineOnIpadEnabled":"true","trailersVideoIdLoggingFixEnabled":"true","postPlayPreviewsEnabled":"false","bypassContextualAssetsEnabled":"false","roarEnabled":"false","useSeason1AltLabelEnabled":"false","disableCDSSearchPaginationSectionKinds":["searchVideoCarousel"],"cdsSearchHorizontalPaginationEnabled":"true","searchPreQueryGamesEnabled":"true","kidsMyListEnabled":"true","billboardEnabled":"true","useCDSGalleryEnabled":"true","contentWarningEnabled":"true","videosInPopularGamesEnabled":"true","avifFormatEnabled":"false","sharksEnabled":"true"}',
    "device_type": "NFAPPL-02-",
    "esn": "NFAPPL-02-IPHONE8%3D1-PXA-02026U9VV5O8AUKEAEO8PUJETCGDD4PQRI9DEB3MDLEMD0EACM4CS78LMD334MN3MQ3NMJ8SU9O9MVGS6BJCURM1PH1MUTGDPF4S4200",
    "idiom": "phone",
    "iosVersion": "15.8.5",
    "isTablet": "false",
    "languages": "en-US",
    "locale": "en-US",
    "maxDeviceWidth": "375",
    "model": "saget",
    "modelType": "IPHONE8-1",
    "odpAware": "true",
    "path": '["account","token","default"]',
    "pathFormat": "graph",
    "pixelDensity": "2.0",
    "progressive": "false",
    "responseFormat": "json",
}
BASE_HEADERS = {
    "User-Agent": "Argo/15.48.1 (iPhone; iOS 15.8.5; Scale/2.00)",
    "x-netflix.request.attempt": "1",
    "x-netflix.request.client.user.guid": "A4CS633D7VCBPE2GPK2HL4EKOE",
    "x-netflix.context.profile-guid": "A4CS633D7VCBPE2GPK2HL4EKOE",
    "x-netflix.request.routing": '{"path":"/nq/mobile/nqios/~15.48.0/user","control_tag":"iosui_argo"}',
    "x-netflix.context.app-version": "15.48.1",
    "x-netflix.argo.translated": "true",
    "x-netflix.context.form-factor": "phone",
    "x-netflix.context.sdk-version": "2012.4",
    "x-netflix.client.appversion": "15.48.1",
    "x-netflix.context.max-device-width": "375",
    "x-netflix.context.ab-tests": "",
    "x-netflix.tracing.cl.useractionid": "4DC655F2-9C3C-4343-8229-CA1B003C3053",
    "x-netflix.client.type": "argo",
    "x-netflix.client.ftl.esn": "NFAPPL-02-IPHONE8=1-PXA-02026U9VV5O8AUKEAEO8PUJETCGDD4PQRI9DEB3MDLEMD0EACM4CS78LMD334MN3MQ3NMJ8SU9O9MVGS6BJCURM1PH1MUTGDPF4S4200",
    "x-netflix.context.locales": "en-US",
    "x-netflix.context.top-level-uuid": "90AFE39F-ADF1-4D8A-B33E-528730990FE3",
    "x-netflix.client.iosversion": "15.8.5",
    "accept-language": "en-US;q=1",
    "x-netflix.argo.abtests": "",
    "x-netflix.context.os-version": "15.8.5",
    "x-netflix.request.client.context": '{"appState":"foreground"}',
    "x-netflix.context.ui-flavor": "argo",
    "x-netflix.argo.nfnsm": "9",
    "x-netflix.context.pixel-density": "2.0",
    "x-netflix.request.toplevel.uuid": "90AFE39F-ADF1-4D8A-B33E-528730990FE3",
    "x-netflix.request.client.timezoneid": "Asia/Dhaka",
}

NETSCAPE_HEADER = ""

HTML_PAGE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cookie Converter & NFToken</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{--bg:#0d0f11;--panel:#15181c;--panel-2:#1b1f24;--line:#2a2f36;--text:#e7e9ec;--muted:#8b939e;--accent:#6ee7b7;--error:#f27272;--mono:'IBM Plex Mono',monospace;--display:'Space Grotesk',sans-serif}
*{box-sizing:border-box}html,body{margin:0;padding:0}body{background:var(--bg);color:var(--text);font-family:var(--mono);min-height:100vh}
.wrap{max-width:1000px;margin:0 auto;padding:48px 20px 64px}
header{display:flex;align-items:baseline;justify-content:space-between;gap:16px;margin-bottom:28px;flex-wrap:wrap}
h1{font-family:var(--display);font-weight:700;font-size:22px;margin:0}h1 span{color:var(--accent)}
header .tag{font-size:12px;color:var(--muted)}
.tabs{display:flex;gap:10px;margin-bottom:20px;border-bottom:1px solid var(--line);flex-wrap:wrap}
.tab-btn{background:none;border:none;color:var(--muted);font-family:var(--mono);font-size:14px;padding:10px 15px;cursor:pointer;border-bottom:2px solid transparent;margin-bottom:-1px}
.tab-btn:hover{color:var(--text)}.tab-btn.active{color:var(--accent);border-bottom-color:var(--accent)}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:20px;margin-bottom:20px;display:none}
.panel.active{display:block}
.controls{display:flex;align-items:center;gap:10px;margin-bottom:16px;flex-wrap:wrap}
select,input[type=text]{font-family:var(--mono);font-size:13px;background:var(--panel-2);border:1px solid var(--line);color:var(--text);padding:8px 10px;border-radius:6px}
select:focus,input[type=text]:focus{outline:1px solid var(--accent)}
.arrow-icon{color:var(--muted);font-size:14px}
button.icon-btn{background:transparent;border:1px solid var(--line);color:var(--muted);width:30px;height:30px;border-radius:6px;cursor:pointer;font-size:14px;display:flex;align-items:center;justify-content:center;margin-left:auto}
button.icon-btn:hover{border-color:var(--accent);color:var(--accent)}
.opts{display:flex;gap:10px;margin-bottom:14px;flex-wrap:wrap;align-items:center}.opts.hidden{display:none}
.opts input[type=text]{width:150px}.opts label{font-size:11px;color:var(--muted);display:flex;align-items:center;gap:6px;margin:0}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}@media(max-width:700px){.grid{grid-template-columns:1fr}}
.field-label{font-size:11px;color:var(--muted);margin-bottom:6px;display:flex;justify-content:space-between}
textarea{width:100%;min-height:280px;resize:vertical;font-family:var(--mono);font-size:12.5px;line-height:1.6;background:var(--panel-2);border:1px solid var(--line);border-radius:8px;padding:12px;color:var(--text)}
textarea::placeholder{color:#545a63}textarea:focus{outline:1px solid var(--accent)}textarea[readonly]{color:var(--accent)}
.actions{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-top:12px}
.upload-link{font-family:var(--mono);font-size:12px;color:var(--muted);cursor:pointer;text-decoration:underline;text-underline-offset:3px;background:none;border:none;padding:0}
.upload-link:hover{color:var(--accent)}
button.btn{font-family:var(--mono);font-size:12.5px;padding:8px 14px;border-radius:6px;border:1px solid var(--line);background:var(--panel-2);color:var(--text);cursor:pointer}
button.btn:hover{border-color:var(--muted)}button.btn.primary{background:var(--accent);color:var(--bg);border-color:var(--accent);font-weight:600}
button.btn.primary:hover{opacity:0.9}button.btn:disabled{opacity:0.5;cursor:not-allowed}
.error{display:none;margin-top:12px;font-size:12.5px;color:var(--error);background:#2a1616;border:1px solid #4a2323;padding:10px 12px;border-radius:6px;white-space:pre-wrap}
.nf-result{background:var(--panel-2);border:1px solid var(--line);border-radius:8px;padding:16px;min-height:280px;display:none;flex-direction:column;gap:14px}
.nf-result.visible{display:flex}
.nf-link-box{word-break:break-all;font-size:13px;line-height:1.5}
.nf-link-box a{color:var(--accent);text-decoration:none}.nf-link-box a:hover{text-decoration:underline}
.nf-meta{font-size:12px;color:var(--muted)}.nf-actions{display:flex;gap:8px;margin-top:auto}
.credits{font-size:11px;color:var(--muted)}
.extract-box{background:var(--panel-2);border:1px solid var(--line);border-radius:8px;padding:24px;text-align:center}
.extract-box input[type=file]{display:none}
.drop-zone{border:2px dashed var(--line);border-radius:8px;padding:40px 20px;cursor:pointer;transition:border-color .2s}
.drop-zone:hover,.drop-zone.dragover{border-color:var(--accent)}
.drop-zone p{margin:8px 0 0;color:var(--muted);font-size:13px}
.extract-controls{display:flex;gap:12px;align-items:center;justify-content:center;margin-top:20px;flex-wrap:wrap}
.extract-controls label{font-size:13px;color:var(--muted)}.extract-controls input[type=text]{width:180px}
.status-box{margin-top:20px;font-size:13px;color:var(--muted);white-space:pre-wrap;text-align:left;background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:12px;display:none}
.status-box.visible{display:block}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>cookie<span>.</span>convert <span style="color:var(--muted);font-weight:500;font-size:16px;"></span></h1>
    <span class="tag" id="countTag">0 cookies</span>
  </header>
  <div class="tabs">
    <button class="tab-btn active" data-tab="converter">Cookie Converter</button>
    <button class="tab-btn" data-tab="nftoken">NFToken Generator</button>
    <button class="tab-btn" data-tab="extractor">Cookie Extractor</button>
  </div>

  <section class="panel active" id="converter">
    <div class="controls">
      <select id="fromFormat">
        <option value="auto" selected>auto-detect</option>
        <option value="netscape">netscape</option>
        <option value="json">json</option>
        <option value="header">header</option>
      </select>
      <span class="arrow-icon">→</span>
      <select id="toFormat">
        <option value="json" selected>json</option>
        <option value="netscape">netscape</option>
        <option value="header">header</option>
      </select>
      <button class="icon-btn" id="swapBtn" title="swap">⇄</button>
    </div>
    <div class="opts hidden" id="headerOpts">
      <input type="text" id="optDomain" placeholder="domain, e.g. .example.com">
      <input type="text" id="optPath" placeholder="path" value="/">
      <label><input type="checkbox" id="optSecure" checked> secure</label>
    </div>
    <div class="grid">
      <div>
        <div class="field-label"><span>input</span><span id="detectTag"></span></div>
        <textarea id="input" placeholder="paste cookies.txt, JSON, or a Cookie: header…"></textarea>
      </div>
      <div>
        <div class="field-label"><span>output</span></div>
        <textarea id="output" readonly placeholder="→"></textarea>
      </div>
    </div>
    <div class="error" id="errorBanner"></div>
    <div class="actions">
      <label class="upload-link" for="fileInput">upload a file instead</label>
      <input type="file" id="fileInput" style="display:none">
      <button class="btn" id="copyBtn">copy output</button>
    </div>
  </section>

  <section class="panel" id="nftoken">
    <div class="grid">
      <div>
        <div class="field-label"><span>cookies input</span></div>
        <textarea id="nfInput" placeholder="paste Netflix cookies here (json / netscape / header)..."></textarea>
      </div>
      <div>
        <div class="field-label"><span>result</span></div>
        <textarea id="nfOutput" readonly placeholder="Login URL and expiry will appear here..." style="display:block;"></textarea>
        <div class="nf-result" id="nfResultBox">
          <div class="nf-link-box">
            <strong>Login URL:</strong><br>
            <a id="nfLink" href="#" target="_blank" rel="noopener"></a>
          </div>
          <div class="nf-meta" id="nfExpiry"></div>
          <div class="nf-actions">
            <button class="btn primary" id="copyLinkBtn">Copy Link</button>
            <button class="btn" id="openLinkBtn">Open Link</button>
          </div>
        </div>
      </div>
    </div>
    <div class="error" id="nfErrorBanner"></div>
    <div class="actions">
      <span class="credits">By rexzy</span>
      <button class="btn primary" id="fetchNfBtn">Fetch NFToken</button>
    </div>
  </section>

  <section class="panel" id="extractor">
    <div class="extract-box">
      <div class="drop-zone" id="dropZone">
        <div style="font-size:28px;margin-bottom:8px;">📦</div>
        <strong>Drop .zip here or click to select</strong>
        <p>Expected structure: Folder → Cookies → *.txt<br>Supports large zips</p>
        <input type="file" id="zipInput" accept=".zip">
      </div>
      <div class="extract-controls">
        <label>Domain filter:</label>
        <input type="text" id="domainFilter" value="spotify.com" placeholder="e.g. spotify.com">
        <button class="btn primary" id="extractBtn" disabled>Extract Cookies</button>
      </div>
      <div class="status-box" id="extractStatus"></div>
    </div>
    <div class="actions" style="margin-top:16px;">
      <span class="credits">By rexzy</span>
    </div>
  </section>
</div>

<script>
(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory();else root.CookieConvert=factory();})(typeof self!=='undefined'?self:this,function(){
'use strict';
var NETSCAPE_HEADER='# Netscape HTTP Cookie File\n# Generated by cookie-convert. Edit at your own risk.\n\n';
function toBool(v){if(typeof v==='boolean')return v;if(typeof v==='string')return v.trim().toUpperCase()==='TRUE';return Boolean(v);}
function normalizeSameSite(v){if(!v)return undefined;var s=String(v).toLowerCase();if(s.startsWith('lax'))return 'Lax';if(s.startsWith('strict'))return 'Strict';if(s.startsWith('none'))return 'None';if(s==='no_restriction')return 'None';if(s==='unspecified')return undefined;return undefined;}
function parseNetscape(text){
  var cookies=[];var lines=text.split(/\r?\n/);
  for(var i=0;i<lines.length;i++){
    var line=lines[i].trim();if(!line)continue;
    var workingLine=line;var httpOnly=false;
    if(line.startsWith('#HttpOnly_')){httpOnly=true;workingLine=line.slice(10);}
    else if(line.startsWith('#'))continue;
    var parts=workingLine.split(/\t+/);
    if(parts.length<7)parts=workingLine.split(/\s{2,}|\t+/);
    if(parts.length<7){parts=workingLine.split(/\s+/);if(parts.length>7)parts=parts.slice(0,6).concat(parts.slice(6).join(' '));}
    if(parts.length<7)continue;
    var domain=parts[0],subdomainsFlag=parts[1],path=parts[2],secureFlag=parts[3],expiresStr=parts[4],name=parts[5],value=parts.slice(6).join(' ');
    var expiresNum=parseInt(expiresStr,10);
    cookies.push({domain:domain,hostOnly:!toBool(subdomainsFlag),path:path||'/',secure:toBool(secureFlag),httpOnly:httpOnly,expires:Number.isFinite(expiresNum)&&expiresNum>0?expiresNum:null,name:name,value:value,sameSite:undefined});
  }
  return cookies;
}
function toNetscape(cookies){
  var lines=cookies.map(function(c){var domain=c.domain||'';var includeSubdomains=c.hostOnly?'FALSE':'TRUE';var path=c.path||'/';var secure=c.secure?'TRUE':'FALSE';var expires=c.expires?String(Math.floor(c.expires)):'0';var namePrefix=c.httpOnly?'#HttpOnly_':'';return [namePrefix+domain,includeSubdomains,path,secure,expires,c.name,c.value].join('\t');});
  return NETSCAPE_HEADER+lines.join('\n')+(lines.length?'\n':'');
}
function parseJSONCookies(text){
  var data;try{data=typeof text==='string'?JSON.parse(text):text;}catch(e){throw new Error('Invalid JSON: '+e.message);}
  var arr=Array.isArray(data)?data:(data&&Array.isArray(data.cookies)?data.cookies:null);
  if(!arr)throw new Error('JSON must be an array of cookies, or an object with a "cookies" array.');
  return arr.map(function(raw){
    var domain=raw.domain||raw.Domain||'';var path=raw.path||raw.Path||'/';
    var secure=toBool(raw.secure!==undefined?raw.secure:(raw.Secure!==undefined?raw.Secure:false));
    var httpOnly=toBool(raw.httpOnly!==undefined?raw.httpOnly:(raw.HttpOnly!==undefined?raw.HttpOnly:false));
    var hostOnly=raw.hostOnly!==undefined?toBool(raw.hostOnly):!(domain.startsWith('.'));
    var expires=null;
    if(raw.session===true||raw.Session===true)expires=null;
    else if(raw.expirationDate!==undefined)expires=Math.floor(Number(raw.expirationDate));
    else if(raw.expires!==undefined&&raw.expires!==-1&&raw.expires!==null){var n=Number(raw.expires);if(Number.isFinite(n))expires=n>1e12?Math.floor(n/1000):Math.floor(n);else{var parsed=Date.parse(raw.expires);expires=Number.isFinite(parsed)?Math.floor(parsed/1000):null;}}
    else if(raw['Expires / Max-Age']){var parsed2=Date.parse(raw['Expires / Max-Age']);expires=Number.isFinite(parsed2)?Math.floor(parsed2/1000):null;}
    return{domain:domain,path:path,secure:secure,httpOnly:httpOnly,hostOnly:hostOnly,expires:expires,sameSite:normalizeSameSite(raw.sameSite||raw.SameSite),name:raw.name||raw.Name,value:raw.value!==undefined?raw.value:raw.Value};
  });
}
function toJSON(cookies,pretty){if(pretty===undefined)pretty=true;var out=cookies.map(function(c){var obj={domain:c.domain||'',hostOnly:!!c.hostOnly,httpOnly:!!c.httpOnly,name:c.name,path:c.path||'/',sameSite:c.sameSite||'unspecified',secure:!!c.secure,session:c.expires===null||c.expires===undefined,value:c.value};if(c.expires)obj.expirationDate=c.expires;return obj;});return JSON.stringify(out,null,pretty?2:0);}
function parseHeader(text,options){options=options||{};var cleaned=text.replace(/^\s*Cookie:\s*/i,'').trim();if(!cleaned)return[];var pairs=cleaned.split(';').map(function(p){return p.trim();}).filter(Boolean);return pairs.map(function(pair){var idx=pair.indexOf('=');var name=idx===-1?pair:pair.slice(0,idx);var value=idx===-1?'':pair.slice(idx+1);return{domain:options.domain||'',path:options.path||'/',secure:options.secure!==undefined?options.secure:true,httpOnly:false,hostOnly:options.hostOnly!==undefined?options.hostOnly:true,expires:options.expires!==undefined?options.expires:null,sameSite:undefined,name:name.trim(),value:value.trim()};});}
function toHeader(cookies){return cookies.map(function(c){return c.name+'='+c.value;}).join('; ');}
function parse(text,format,options){switch(format){case'netscape':return parseNetscape(text);case'json':return parseJSONCookies(text);case'header':return parseHeader(text,options);default:throw new Error('Unknown source format "'+format+'".');}}
function serialize(cookies,format,options){options=options||{};switch(format){case'netscape':return toNetscape(cookies);case'json':return toJSON(cookies,options.pretty!==false);case'header':return toHeader(cookies);default:throw new Error('Unknown target format "'+format+'".');}}
function detectFormat(text){var t=text.trim();if(!t)return null;if(t.startsWith('[')||t.startsWith('{'))return'json';if(t.startsWith('# Netscape')||t.startsWith('#HttpOnly_')||/^[^\s]+\t(TRUE|FALSE)\t/im.test(t))return'netscape';if(/^[^\s]+\s+(TRUE|FALSE)\s+\/\S*\s+(TRUE|FALSE)\s+\d+\s+\S+/im.test(t))return'netscape';if(/^[^=;\n]+=[^;\n]*(;\s*[^=;\n]+=[^;\n]*)*$/.test(t.split('\n')[0]))return'header';return null;}
function convert(text,from,to,options){options=options||{};var source=from==='auto'?detectFormat(text):from;if(!source)throw new Error('Could not auto-detect the source format. Please choose it explicitly.');var cookies=parse(text,source,options);var output=serialize(cookies,to,options);return{cookies:cookies,output:output,detected:source};}
return{parse:parse,serialize:serialize,convert:convert,detectFormat:detectFormat};
});

document.addEventListener('DOMContentLoaded',function(){
  var $=function(id){return document.getElementById(id);};

  document.querySelectorAll('.tab-btn').forEach(function(btn){
    btn.addEventListener('click',function(){
      document.querySelectorAll('.tab-btn').forEach(function(b){b.classList.remove('active');});
      document.querySelectorAll('.panel').forEach(function(p){p.classList.remove('active');});
      btn.classList.add('active');
      $(btn.dataset.tab).classList.add('active');
    });
  });

  // Converter
  var input=$('input'),output=$('output'),fromSel=$('fromFormat'),toSel=$('toFormat');
  var errorBanner=$('errorBanner'),countTag=$('countTag'),detectTag=$('detectTag'),headerOpts=$('headerOpts');
  function toggleHeaderOpts(){if(fromSel.value==='header')headerOpts.classList.remove('hidden');else headerOpts.classList.add('hidden');}
  fromSel.addEventListener('change',toggleHeaderOpts);toggleHeaderOpts();
  function showError(msg){if(!msg){errorBanner.style.display='none';errorBanner.textContent='';return;}errorBanner.style.display='block';errorBanner.textContent=msg;}
  function runConversion(){
    showError('');var text=input.value;
    if(!text||!text.trim()){output.value='';countTag.textContent='0 cookies';detectTag.textContent='';return;}
    var from=fromSel.value,to=toSel.value;
    var options={domain:$('optDomain').value||undefined,path:$('optPath').value||undefined,secure:$('optSecure').checked};
    try{var result=window.CookieConvert.convert(text,from,to,options);output.value=result.output;var count=result.cookies.length;countTag.textContent=count+' cookie'+(count===1?'':'s');detectTag.textContent=from==='auto'?result.detected:'';}
    catch(err){output.value='';countTag.textContent='0 cookies';showError(err.message);}
  }
  function debounce(fn,ms){var t;return function(){var args=arguments,ctx=this;clearTimeout(t);t=setTimeout(function(){fn.apply(ctx,args);},ms);};}
  input.addEventListener('input',debounce(runConversion,200));
  fromSel.addEventListener('change',runConversion);toSel.addEventListener('change',runConversion);
  $('optDomain').addEventListener('input',debounce(runConversion,200));$('optPath').addEventListener('input',debounce(runConversion,200));$('optSecure').addEventListener('change',runConversion);
  $('swapBtn').addEventListener('click',function(){if(fromSel.value==='auto')return;var f=fromSel.value,t=toSel.value;fromSel.value=t;toSel.value=f;input.value=output.value;toggleHeaderOpts();runConversion();});
  $('copyBtn').addEventListener('click',async function(){if(!output.value)return;try{await navigator.clipboard.writeText(output.value);var btn=$('copyBtn');var old=btn.textContent;btn.textContent='copied';setTimeout(function(){btn.textContent=old;},1000);}catch(e){showError('Clipboard access denied.');}});
  $('fileInput').addEventListener('change',function(e){var file=e.target.files[0];if(!file)return;var reader=new FileReader();reader.onload=function(ev){input.value=ev.target.result;runConversion();};reader.readAsText(file);});

  // NFToken
  var currentLoginUrl='';
  function showNfResult(url,expiryStr){$('nfOutput').style.display='none';$('nfResultBox').classList.add('visible');var link=$('nfLink');link.href=url;link.textContent=url;currentLoginUrl=url;$('nfExpiry').textContent='Expires: '+expiryStr;}
  function hideNfResult(){$('nfResultBox').classList.remove('visible');$('nfOutput').style.display='block';$('nfOutput').value='';}
  $('fetchNfBtn').addEventListener('click',async function(){
    var nfInput=$('nfInput').value.trim();var nfError=$('nfErrorBanner');
    nfError.style.display='none';nfError.textContent='';hideNfResult();$('nfOutput').value='Fetching...';
    if(!nfInput){$('nfOutput').value='';nfError.style.display='block';nfError.textContent='Paste some Netflix cookies first.';return;}
    try{
      var response=await fetch('/api/nftoken',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({cookie:nfInput})});
      var data=await response.json();
      if(!response.ok||data.error)throw new Error(data.error||('Request failed with status '+response.status));
      var date=new Date(data.expires*1000);var pad=function(n){return String(n).padStart(2,'0');};
      var expiryStr=date.getFullYear()+'-'+pad(date.getMonth()+1)+'-'+pad(date.getDate())+' '+pad(date.getHours())+':'+pad(date.getMinutes())+':'+pad(date.getSeconds());
      showNfResult(data.loginUrl,expiryStr);
    }catch(err){hideNfResult();nfError.style.display='block';nfError.textContent=err.message;}
  });
  $('copyLinkBtn').addEventListener('click',async function(){if(!currentLoginUrl)return;try{await navigator.clipboard.writeText(currentLoginUrl);var btn=$('copyLinkBtn');var old=btn.textContent;btn.textContent='Copied!';setTimeout(function(){btn.textContent=old;},1200);}catch(e){alert('Clipboard access denied');}});
  $('openLinkBtn').addEventListener('click',function(){if(currentLoginUrl)window.open(currentLoginUrl,'_blank');});

  // Extractor
  var zipFile=null;var dropZone=$('dropZone');var zipInput=$('zipInput');var extractBtn=$('extractBtn');var statusBox=$('extractStatus');
  dropZone.addEventListener('click',function(){zipInput.click();});
  dropZone.addEventListener('dragover',function(e){e.preventDefault();dropZone.classList.add('dragover');});
  dropZone.addEventListener('dragleave',function(){dropZone.classList.remove('dragover');});
  dropZone.addEventListener('drop',function(e){e.preventDefault();dropZone.classList.remove('dragover');if(e.dataTransfer.files.length)handleZip(e.dataTransfer.files[0]);});
  zipInput.addEventListener('change',function(){if(zipInput.files.length)handleZip(zipInput.files[0]);});
  function handleZip(file){if(!file.name.toLowerCase().endsWith('.zip')){alert('Please select a .zip file');return;}zipFile=file;dropZone.querySelector('strong').textContent=file.name;dropZone.querySelector('p').textContent=(file.size/1024/1024).toFixed(1)+' MB — ready';extractBtn.disabled=false;statusBox.classList.remove('visible');}
  extractBtn.addEventListener('click',async function(){
    if(!zipFile)return;extractBtn.disabled=true;extractBtn.textContent='Uploading...';statusBox.classList.add('visible');statusBox.textContent='Uploading zip...';
    var domain=$('domainFilter').value.trim()||'spotify.com';
    try{
      var form=new FormData();form.append('zip',zipFile);form.append('domain',domain);
      var response=await fetch('/api/extract',{method:'POST',body:form});
      if(!response.ok){var err=await response.json().catch(function(){return{error:'Server error '+response.status};});throw new Error(err.error||'Extraction failed');}
      var blob=await response.blob();var url=URL.createObjectURL(blob);var a=document.createElement('a');a.href=url;a.download='extracted_cookies.zip';document.body.appendChild(a);a.click();a.remove();URL.revokeObjectURL(url);
      var count=response.headers.get('X-Extracted-Count')||'?';statusBox.textContent='Done! Extracted cookies from '+count+' folders.\nDownloaded: extracted_cookies.zip';
    }catch(err){statusBox.textContent='Error: '+err.message;}finally{extractBtn.disabled=false;extractBtn.textContent='Extract Cookies';}
  });
});
</script>
</body>
</html>
'''

def parse_multipart(rfile, content_type, content_length):
    boundary = None
    for part in content_type.split(';'):
        part = part.strip()
        if part.startswith('boundary='):
            boundary = part[9:].strip().strip('"')
            break
    if not boundary:
        raise ValueError("No boundary found")

    boundary_bytes = ('--' + boundary).encode('utf-8')
    tmp_in = tempfile.NamedTemporaryFile(delete=False)
    remaining = content_length
    while remaining > 0:
        chunk = rfile.read(min(1024*1024, remaining))
        if not chunk: break
        tmp_in.write(chunk)
        remaining -= len(chunk)
    tmp_in.close()

    domain = 'spotify.com'
    zip_path = None
    try:
        with open(tmp_in.name, 'rb') as f:
            data = f.read()
        parts = data.split(boundary_bytes)
        for part in parts:
            if not part or part.startswith(b'--'): continue
            if b'\r\n\r\n' not in part: continue
            header_blob, body = part.split(b'\r\n\r\n', 1)
            headers = header_blob.decode('utf-8', errors='ignore')
            if body.endswith(b'\r\n'): body = body[:-2]
            if 'name="domain"' in headers:
                domain = body.decode('utf-8', errors='ignore').strip() or 'spotify.com'
            elif 'name="zip"' in headers or 'filename=' in headers:
                zip_fd, zip_path = tempfile.mkstemp(suffix='.zip')
                with os.fdopen(zip_fd, 'wb') as zf:
                    zf.write(body)
    finally:
        try: os.unlink(tmp_in.name)
        except: pass

    if not zip_path:
        raise ValueError("No zip file found in upload")
    return zip_path, domain


class ServerHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/nftoken':
            self.handle_nftoken()
        elif self.path == '/api/extract':
            self.handle_extract()
        else:
            self.send_response(404)
            self.end_headers()

    def handle_nftoken(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            payload = json.loads(post_data.decode('utf-8'))
            cookie_str = payload.get('cookie', '').strip()
            if not cookie_str:
                raise ValueError("No cookie data provided")

            netflix_id = None
            try:
                data = json.loads(cookie_str)
                if isinstance(data, list):
                    for c in data:
                        if (c.get('name') or c.get('Name') or '').strip() == 'NetflixId':
                            netflix_id = c.get('value') or c.get('Value')
                            break
                elif isinstance(data, dict) and 'cookies' in data:
                    for c in data['cookies']:
                        if (c.get('name') or c.get('Name') or '').strip() == 'NetflixId':
                            netflix_id = c.get('value') or c.get('Value')
                            break
            except: pass

            if not netflix_id:
                m = re.search(r'(?:^|[;\s])NetflixId=([^;,\s]+)', cookie_str, re.I)
                if m: netflix_id = m.group(1)

            if not netflix_id:
                for line in cookie_str.splitlines():
                    line = line.strip()
                    if not line or line.startswith('#'): continue
                    parts = re.split(r'[\t\s]+', line)
                    if len(parts) >= 7 and parts[5] == 'NetflixId':
                        netflix_id = ' '.join(parts[6:])
                        break

            if not netflix_id:
                raise ValueError("Missing required cookie: NetflixId")

            headers = dict(BASE_HEADERS)
            proxies = {"http": PROXY_URL, "https": PROXY_URL}
            response = requests.get(API_URL, params=QUERY_PARAMS, headers=headers,
                                    cookies={"NetflixId": netflix_id}, proxies=proxies,
                                    timeout=30, verify=False)
            response.raise_for_status()
            data = response.json()
            token_data = (((data.get("value") or {}).get("account") or {}).get("token") or {}).get("default") or {}
            token = token_data.get("token")
            expires = token_data.get("expires")
            if not token:
                raise ValueError("No token found in Netflix response")
            if isinstance(expires, (int, float)) and expires > 1e12:
                expires = int(expires // 1000)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"loginUrl": "https://netflix.com/?nftoken=" + token, "expires": expires}).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def handle_extract(self):
        zip_path = None
        try:
            content_type = self.headers.get('Content-Type', '')
            content_length = int(self.headers.get('Content-Length', 0))
            if 'multipart/form-data' not in content_type:
                raise ValueError("Expected multipart form data")
            if content_length > 3 * 1024 * 1024 * 1024:
                raise ValueError("File too large (max 3 GB)")

            zip_path, domain = parse_multipart(self.rfile, content_type, content_length)
            domain = domain.lower().strip() or 'spotify.com'

            results = {}
            with zipfile.ZipFile(zip_path, 'r') as zf:
                for name in zf.namelist():
                    parts = name.replace('\\', '/').split('/')
                    if len(parts) >= 3 and parts[-2].lower() == 'cookies' and parts[-1].lower().endswith('.txt'):
                        parent = parts[-3]
                        if not parent or parent == '.': continue
                        try:
                            content = zf.read(name).decode('utf-8', errors='ignore')
                        except: continue
                        matching = [l for l in content.splitlines() if domain in l.lower()]
                        if matching:
                            results.setdefault(parent, []).extend(matching)

            if not results:
                raise ValueError(f"No cookies containing '{domain}' found")

            out_buffer = io.BytesIO()
            with zipfile.ZipFile(out_buffer, 'w', zipfile.ZIP_DEFLATED) as out_zf:
                for folder, lines in results.items():
                    safe = re.sub(r'[<>:"/\\|?*]', '_', folder) + '.txt'
                    out_zf.writestr(safe, NETSCAPE_HEADER + '\n'.join(lines) + '\n')

            out_data = out_buffer.getvalue()
            self.send_response(200)
            self.send_header('Content-Type', 'application/zip')
            self.send_header('Content-Disposition', 'attachment; filename="extracted_cookies.zip"')
            self.send_header('X-Extracted-Count', str(len(results)))
            self.send_header('Content-Length', str(len(out_data)))
            self.end_headers()
            self.wfile.write(out_data)
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
        finally:
            if zip_path and os.path.exists(zip_path):
                try: os.unlink(zip_path)
                except: pass

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {args[0]}")


if __name__ == '__main__':
    print(f"Serving at http://127.0.0.1:{PORT}")
    with http.server.HTTPServer(("127.0.0.1", PORT), ServerHandler) as httpd:
        httpd.serve_forever()