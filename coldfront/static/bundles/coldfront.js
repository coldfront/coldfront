import{g as Io,r as Oo,$ as G,D as Ka}from"./c3.js";import{d as No,g as Mo}from"./util.js";var Un={exports:{}};var Yn=typeof window<"u"&&typeof document<"u"&&typeof navigator<"u",xo=(function(){for(var t=["Edge","Trident","Firefox"],i=0;i<t.length;i+=1)if(Yn&&navigator.userAgent.indexOf(t[i])>=0)return 1;return 0})();function ko(t){var i=!1;return function(){i||(i=!0,window.Promise.resolve().then(function(){i=!1,t()}))}}function Lo(t){var i=!1;return function(){i||(i=!0,setTimeout(function(){i=!1,t()},xo))}}var Fo=Yn&&window.Promise,Po=Fo?ko:Lo;function ai(t){var i={};return t&&i.toString.call(t)==="[object Function]"}function qe(t,i){if(t.nodeType!==1)return[];var e=t.ownerDocument.defaultView,d=e.getComputedStyle(t,null);return i?d[i]:d}function la(t){return t.nodeName==="HTML"?t:t.parentNode||t.host}function qn(t){if(!t)return document.body;switch(t.nodeName){case"HTML":case"BODY":return t.ownerDocument.body;case"#document":return t.body}var i=qe(t),e=i.overflow,d=i.overflowX,m=i.overflowY;return/(auto|scroll|overlay)/.test(e+m+d)?t:qn(la(t))}function ii(t){return t&&t.referenceNode?t.referenceNode:t}var za=Yn&&!!(window.MSInputMethodContext&&document.documentMode),Ga=Yn&&/MSIE 10/.test(navigator.userAgent);function pn(t){return t===11?za:t===10?Ga:za||Ga}function dn(t){if(!t)return document.documentElement;for(var i=pn(10)?document.body:null,e=t.offsetParent||null;e===i&&t.nextElementSibling;)e=(t=t.nextElementSibling).offsetParent;var d=e&&e.nodeName;return!d||d==="BODY"||d==="HTML"?t?t.ownerDocument.documentElement:document.documentElement:["TH","TD","TABLE"].indexOf(e.nodeName)!==-1&&qe(e,"position")==="static"?dn(e):e}function Ro(t){var i=t.nodeName;return i==="BODY"?!1:i==="HTML"||dn(t.firstElementChild)===t}function ia(t){return t.parentNode!==null?ia(t.parentNode):t}function pt(t,i){if(!t||!t.nodeType||!i||!i.nodeType)return document.documentElement;var e=t.compareDocumentPosition(i)&Node.DOCUMENT_POSITION_FOLLOWING,d=e?t:i,m=e?i:t,h=document.createRange();h.setStart(d,0),h.setEnd(m,0);var a=h.commonAncestorContainer;if(t!==a&&i!==a||d.contains(m))return Ro(a)?a:dn(a);var E=ia(t);return E.host?pt(E.host,i):pt(t,ia(i).host)}function fn(t){var i=arguments.length>1&&arguments[1]!==void 0?arguments[1]:"top",e=i==="top"?"scrollTop":"scrollLeft",d=t.nodeName;if(d==="BODY"||d==="HTML"){var m=t.ownerDocument.documentElement,h=t.ownerDocument.scrollingElement||m;return h[e]}return t[e]}function jo(t,i){var e=arguments.length>2&&arguments[2]!==void 0?arguments[2]:!1,d=fn(i,"top"),m=fn(i,"left"),h=e?-1:1;return t.top+=d*h,t.bottom+=d*h,t.left+=m*h,t.right+=m*h,t}function Qa(t,i){var e=i==="x"?"Left":"Top",d=e==="Left"?"Right":"Bottom";return parseFloat(t["border"+e+"Width"])+parseFloat(t["border"+d+"Width"])}function Ja(t,i,e,d){return Math.max(i["offset"+t],i["scroll"+t],e["client"+t],e["offset"+t],e["scroll"+t],pn(10)?parseInt(e["offset"+t])+parseInt(d["margin"+(t==="Height"?"Top":"Left")])+parseInt(d["margin"+(t==="Height"?"Bottom":"Right")]):0)}function ri(t){var i=t.body,e=t.documentElement,d=pn(10)&&getComputedStyle(e);return{height:Ja("Height",i,e,d),width:Ja("Width",i,e,d)}}var Uo=function(t,i){if(!(t instanceof i))throw new TypeError("Cannot call a class as a function")},Bo=(function(){function t(i,e){for(var d=0;d<e.length;d++){var m=e[d];m.enumerable=m.enumerable||!1,m.configurable=!0,"value"in m&&(m.writable=!0),Object.defineProperty(i,m.key,m)}}return function(i,e,d){return e&&t(i.prototype,e),d&&t(i,d),i}})(),hn=function(t,i,e){return i in t?Object.defineProperty(t,i,{value:e,enumerable:!0,configurable:!0,writable:!0}):t[i]=e,t},le=Object.assign||function(t){for(var i=1;i<arguments.length;i++){var e=arguments[i];for(var d in e)Object.prototype.hasOwnProperty.call(e,d)&&(t[d]=e[d])}return t};function xe(t){return le({},t,{right:t.left+t.width,bottom:t.top+t.height})}function ra(t){var i={};try{if(pn(10)){i=t.getBoundingClientRect();var e=fn(t,"top"),d=fn(t,"left");i.top+=e,i.left+=d,i.bottom+=e,i.right+=d}else i=t.getBoundingClientRect()}catch{}var m={left:i.left,top:i.top,width:i.right-i.left,height:i.bottom-i.top},h=t.nodeName==="HTML"?ri(t.ownerDocument):{},a=h.width||t.clientWidth||m.width,E=h.height||t.clientHeight||m.height,C=t.offsetWidth-a,S=t.offsetHeight-E;if(C||S){var b=qe(t);C-=Qa(b,"x"),S-=Qa(b,"y"),m.width-=C,m.height-=S}return xe(m)}function ua(t,i){var e=arguments.length>2&&arguments[2]!==void 0?arguments[2]:!1,d=pn(10),m=i.nodeName==="HTML",h=ra(t),a=ra(i),E=qn(t),C=qe(i),S=parseFloat(C.borderTopWidth),b=parseFloat(C.borderLeftWidth);e&&m&&(a.top=Math.max(a.top,0),a.left=Math.max(a.left,0));var A=xe({top:h.top-a.top-S,left:h.left-a.left-b,width:h.width,height:h.height});if(A.marginTop=0,A.marginLeft=0,!d&&m){var N=parseFloat(C.marginTop),O=parseFloat(C.marginLeft);A.top-=S-N,A.bottom-=S-N,A.left-=b-O,A.right-=b-O,A.marginTop=N,A.marginLeft=O}return(d&&!e?i.contains(E):i===E&&E.nodeName!=="BODY")&&(A=jo(A,i)),A}function Ho(t){var i=arguments.length>1&&arguments[1]!==void 0?arguments[1]:!1,e=t.ownerDocument.documentElement,d=ua(t,e),m=Math.max(e.clientWidth,window.innerWidth||0),h=Math.max(e.clientHeight,window.innerHeight||0),a=i?0:fn(e),E=i?0:fn(e,"left"),C={top:a-d.top+d.marginTop,left:E-d.left+d.marginLeft,width:m,height:h};return xe(C)}function oi(t){var i=t.nodeName;if(i==="BODY"||i==="HTML")return!1;if(qe(t,"position")==="fixed")return!0;var e=la(t);return e?oi(e):!1}function si(t){if(!t||!t.parentElement||pn())return document.documentElement;for(var i=t.parentElement;i&&qe(i,"transform")==="none";)i=i.parentElement;return i||document.documentElement}function ca(t,i,e,d){var m=arguments.length>4&&arguments[4]!==void 0?arguments[4]:!1,h={top:0,left:0},a=m?si(t):pt(t,ii(i));if(d==="viewport")h=Ho(a,m);else{var E=void 0;d==="scrollParent"?(E=qn(la(i)),E.nodeName==="BODY"&&(E=t.ownerDocument.documentElement)):d==="window"?E=t.ownerDocument.documentElement:E=d;var C=ua(E,a,m);if(E.nodeName==="HTML"&&!oi(a)){var S=ri(t.ownerDocument),b=S.height,A=S.width;h.top+=C.top-C.marginTop,h.bottom=b+C.top,h.left+=C.left-C.marginLeft,h.right=A+C.left}else h=C}e=e||0;var N=typeof e=="number";return h.left+=N?e:e.left||0,h.top+=N?e:e.top||0,h.right-=N?e:e.right||0,h.bottom-=N?e:e.bottom||0,h}function Yo(t){var i=t.width,e=t.height;return i*e}function li(t,i,e,d,m){var h=arguments.length>5&&arguments[5]!==void 0?arguments[5]:0;if(t.indexOf("auto")===-1)return t;var a=ca(e,d,h,m),E={top:{width:a.width,height:i.top-a.top},right:{width:a.right-i.right,height:a.height},bottom:{width:a.width,height:a.bottom-i.bottom},left:{width:i.left-a.left,height:a.height}},C=Object.keys(E).map(function(N){return le({key:N},E[N],{area:Yo(E[N])})}).sort(function(N,O){return O.area-N.area}),S=C.filter(function(N){var O=N.width,L=N.height;return O>=e.clientWidth&&L>=e.clientHeight}),b=S.length>0?S[0].key:C[0].key,A=t.split("-")[1];return b+(A?"-"+A:"")}function ui(t,i,e){var d=arguments.length>3&&arguments[3]!==void 0?arguments[3]:null,m=d?si(i):pt(i,ii(e));return ua(e,m,d)}function ci(t){var i=t.ownerDocument.defaultView,e=i.getComputedStyle(t),d=parseFloat(e.marginTop||0)+parseFloat(e.marginBottom||0),m=parseFloat(e.marginLeft||0)+parseFloat(e.marginRight||0),h={width:t.offsetWidth+m,height:t.offsetHeight+d};return h}function mt(t){var i={left:"right",right:"left",bottom:"top",top:"bottom"};return t.replace(/left|right|bottom|top/g,function(e){return i[e]})}function di(t,i,e){e=e.split("-")[0];var d=ci(t),m={width:d.width,height:d.height},h=["right","left"].indexOf(e)!==-1,a=h?"top":"left",E=h?"left":"top",C=h?"height":"width",S=h?"width":"height";return m[a]=i[a]+i[C]/2-d[C]/2,e===E?m[E]=i[E]-d[S]:m[E]=i[mt(E)],m}function Vn(t,i){return Array.prototype.find?t.find(i):t.filter(i)[0]}function qo(t,i,e){if(Array.prototype.findIndex)return t.findIndex(function(m){return m[i]===e});var d=Vn(t,function(m){return m[i]===e});return t.indexOf(d)}function fi(t,i,e){var d=e===void 0?t:t.slice(0,qo(t,"name",e));return d.forEach(function(m){m.function&&console.warn("`modifier.function` is deprecated, use `modifier.fn`!");var h=m.function||m.fn;m.enabled&&ai(h)&&(i.offsets.popper=xe(i.offsets.popper),i.offsets.reference=xe(i.offsets.reference),i=h(i,m))}),i}function Vo(){if(!this.state.isDestroyed){var t={instance:this,styles:{},arrowStyles:{},attributes:{},flipped:!1,offsets:{}};t.offsets.reference=ui(this.state,this.popper,this.reference,this.options.positionFixed),t.placement=li(this.options.placement,t.offsets.reference,this.popper,this.reference,this.options.modifiers.flip.boundariesElement,this.options.modifiers.flip.padding),t.originalPlacement=t.placement,t.positionFixed=this.options.positionFixed,t.offsets.popper=di(this.popper,t.offsets.reference,t.placement),t.offsets.popper.position=this.options.positionFixed?"fixed":"absolute",t=fi(this.modifiers,t),this.state.isCreated?this.options.onUpdate(t):(this.state.isCreated=!0,this.options.onCreate(t))}}function hi(t,i){return t.some(function(e){var d=e.name,m=e.enabled;return m&&d===i})}function da(t){for(var i=[!1,"ms","Webkit","Moz","O"],e=t.charAt(0).toUpperCase()+t.slice(1),d=0;d<i.length;d++){var m=i[d],h=m?""+m+e:t;if(typeof document.body.style[h]<"u")return h}return null}function Wo(){return this.state.isDestroyed=!0,hi(this.modifiers,"applyStyle")&&(this.popper.removeAttribute("x-placement"),this.popper.style.position="",this.popper.style.top="",this.popper.style.left="",this.popper.style.right="",this.popper.style.bottom="",this.popper.style.willChange="",this.popper.style[da("transform")]=""),this.disableEventListeners(),this.options.removeOnDestroy&&this.popper.parentNode.removeChild(this.popper),this}function pi(t){var i=t.ownerDocument;return i?i.defaultView:window}function mi(t,i,e,d){var m=t.nodeName==="BODY",h=m?t.ownerDocument.defaultView:t;h.addEventListener(i,e,{passive:!0}),m||mi(qn(h.parentNode),i,e,d),d.push(h)}function Ko(t,i,e,d){e.updateBound=d,pi(t).addEventListener("resize",e.updateBound,{passive:!0});var m=qn(t);return mi(m,"scroll",e.updateBound,e.scrollParents),e.scrollElement=m,e.eventsEnabled=!0,e}function zo(){this.state.eventsEnabled||(this.state=Ko(this.reference,this.options,this.state,this.scheduleUpdate))}function Go(t,i){return pi(t).removeEventListener("resize",i.updateBound),i.scrollParents.forEach(function(e){e.removeEventListener("scroll",i.updateBound)}),i.updateBound=null,i.scrollParents=[],i.scrollElement=null,i.eventsEnabled=!1,i}function Qo(){this.state.eventsEnabled&&(cancelAnimationFrame(this.scheduleUpdate),this.state=Go(this.reference,this.state))}function fa(t){return t!==""&&!isNaN(parseFloat(t))&&isFinite(t)}function oa(t,i){Object.keys(i).forEach(function(e){var d="";["width","height","top","right","bottom","left"].indexOf(e)!==-1&&fa(i[e])&&(d="px"),t.style[e]=i[e]+d})}function Jo(t,i){Object.keys(i).forEach(function(e){var d=i[e];d!==!1?t.setAttribute(e,i[e]):t.removeAttribute(e)})}function Xo(t){return oa(t.instance.popper,t.styles),Jo(t.instance.popper,t.attributes),t.arrowElement&&Object.keys(t.arrowStyles).length&&oa(t.arrowElement,t.arrowStyles),t}function Zo(t,i,e,d,m){var h=ui(m,i,t,e.positionFixed),a=li(e.placement,h,i,t,e.modifiers.flip.boundariesElement,e.modifiers.flip.padding);return i.setAttribute("x-placement",a),oa(i,{position:e.positionFixed?"fixed":"absolute"}),e}function es(t,i){var e=t.offsets,d=e.popper,m=e.reference,h=Math.round,a=Math.floor,E=function(ee){return ee},C=h(m.width),S=h(d.width),b=["left","right"].indexOf(t.placement)!==-1,A=t.placement.indexOf("-")!==-1,N=C%2===S%2,O=C%2===1&&S%2===1,L=i?b||A||N?h:a:E,M=i?h:E;return{left:L(O&&!A&&i?d.left-1:d.left),top:M(d.top),bottom:M(d.bottom),right:L(d.right)}}var ns=Yn&&/Firefox/i.test(navigator.userAgent);function ts(t,i){var e=i.x,d=i.y,m=t.offsets.popper,h=Vn(t.instance.modifiers,function(K){return K.name==="applyStyle"}).gpuAcceleration;h!==void 0&&console.warn("WARNING: `gpuAcceleration` option moved to `computeStyle` modifier and will not be supported in future versions of Popper.js!");var a=h!==void 0?h:i.gpuAcceleration,E=dn(t.instance.popper),C=ra(E),S={position:m.position},b=es(t,window.devicePixelRatio<2||!ns),A=e==="bottom"?"top":"bottom",N=d==="right"?"left":"right",O=da("transform"),L=void 0,M=void 0;if(A==="bottom"?E.nodeName==="HTML"?M=-E.clientHeight+b.bottom:M=-C.height+b.bottom:M=b.top,N==="right"?E.nodeName==="HTML"?L=-E.clientWidth+b.right:L=-C.width+b.right:L=b.left,a&&O)S[O]="translate3d("+L+"px, "+M+"px, 0)",S[A]=0,S[N]=0,S.willChange="transform";else{var V=A==="bottom"?-1:1,ee=N==="right"?-1:1;S[A]=M*V,S[N]=L*ee,S.willChange=A+", "+N}var Y={"x-placement":t.placement};return t.attributes=le({},Y,t.attributes),t.styles=le({},S,t.styles),t.arrowStyles=le({},t.offsets.arrow,t.arrowStyles),t}function gi(t,i,e){var d=Vn(t,function(E){var C=E.name;return C===i}),m=!!d&&t.some(function(E){return E.name===e&&E.enabled&&E.order<d.order});if(!m){var h="`"+i+"`",a="`"+e+"`";console.warn(a+" modifier is required by "+h+" modifier in order to work, be sure to include it before "+h+"!")}return m}function as(t,i){var e;if(!gi(t.instance.modifiers,"arrow","keepTogether"))return t;var d=i.element;if(typeof d=="string"){if(d=t.instance.popper.querySelector(d),!d)return t}else if(!t.instance.popper.contains(d))return console.warn("WARNING: `arrow.element` must be child of its popper element!"),t;var m=t.placement.split("-")[0],h=t.offsets,a=h.popper,E=h.reference,C=["left","right"].indexOf(m)!==-1,S=C?"height":"width",b=C?"Top":"Left",A=b.toLowerCase(),N=C?"left":"top",O=C?"bottom":"right",L=ci(d)[S];E[O]-L<a[A]&&(t.offsets.popper[A]-=a[A]-(E[O]-L)),E[A]+L>a[O]&&(t.offsets.popper[A]+=E[A]+L-a[O]),t.offsets.popper=xe(t.offsets.popper);var M=E[A]+E[S]/2-L/2,V=qe(t.instance.popper),ee=parseFloat(V["margin"+b]),Y=parseFloat(V["border"+b+"Width"]),K=M-t.offsets.popper[A]-ee-Y;return K=Math.max(Math.min(a[S]-L,K),0),t.arrowElement=d,t.offsets.arrow=(e={},hn(e,A,Math.round(K)),hn(e,N,""),e),t}function is(t){return t==="end"?"start":t==="start"?"end":t}var vi=["auto-start","auto","auto-end","top-start","top","top-end","right-start","right","right-end","bottom-end","bottom","bottom-start","left-end","left","left-start"],Jt=vi.slice(3);function Xa(t){var i=arguments.length>1&&arguments[1]!==void 0?arguments[1]:!1,e=Jt.indexOf(t),d=Jt.slice(e+1).concat(Jt.slice(0,e));return i?d.reverse():d}var Xt={FLIP:"flip",CLOCKWISE:"clockwise",COUNTERCLOCKWISE:"counterclockwise"};function rs(t,i){if(hi(t.instance.modifiers,"inner")||t.flipped&&t.placement===t.originalPlacement)return t;var e=ca(t.instance.popper,t.instance.reference,i.padding,i.boundariesElement,t.positionFixed),d=t.placement.split("-")[0],m=mt(d),h=t.placement.split("-")[1]||"",a=[];switch(i.behavior){case Xt.FLIP:a=[d,m];break;case Xt.CLOCKWISE:a=Xa(d);break;case Xt.COUNTERCLOCKWISE:a=Xa(d,!0);break;default:a=i.behavior}return a.forEach(function(E,C){if(d!==E||a.length===C+1)return t;d=t.placement.split("-")[0],m=mt(d);var S=t.offsets.popper,b=t.offsets.reference,A=Math.floor,N=d==="left"&&A(S.right)>A(b.left)||d==="right"&&A(S.left)<A(b.right)||d==="top"&&A(S.bottom)>A(b.top)||d==="bottom"&&A(S.top)<A(b.bottom),O=A(S.left)<A(e.left),L=A(S.right)>A(e.right),M=A(S.top)<A(e.top),V=A(S.bottom)>A(e.bottom),ee=d==="left"&&O||d==="right"&&L||d==="top"&&M||d==="bottom"&&V,Y=["top","bottom"].indexOf(d)!==-1,K=!!i.flipVariations&&(Y&&h==="start"&&O||Y&&h==="end"&&L||!Y&&h==="start"&&M||!Y&&h==="end"&&V),D=!!i.flipVariationsByContent&&(Y&&h==="start"&&L||Y&&h==="end"&&O||!Y&&h==="start"&&V||!Y&&h==="end"&&M),re=K||D;(N||ee||re)&&(t.flipped=!0,(N||ee)&&(d=a[C+1]),re&&(h=is(h)),t.placement=d+(h?"-"+h:""),t.offsets.popper=le({},t.offsets.popper,di(t.instance.popper,t.offsets.reference,t.placement)),t=fi(t.instance.modifiers,t,"flip"))}),t}function os(t){var i=t.offsets,e=i.popper,d=i.reference,m=t.placement.split("-")[0],h=Math.floor,a=["top","bottom"].indexOf(m)!==-1,E=a?"right":"bottom",C=a?"left":"top",S=a?"width":"height";return e[E]<h(d[C])&&(t.offsets.popper[C]=h(d[C])-e[S]),e[C]>h(d[E])&&(t.offsets.popper[C]=h(d[E])),t}function ss(t,i,e,d){var m=t.match(/((?:\-|\+)?\d*\.?\d*)(.*)/),h=+m[1],a=m[2];if(!h)return t;if(a.indexOf("%")===0){var E=void 0;switch(a){case"%p":E=e;break;case"%":case"%r":default:E=d}var C=xe(E);return C[i]/100*h}else if(a==="vh"||a==="vw"){var S=void 0;return a==="vh"?S=Math.max(document.documentElement.clientHeight,window.innerHeight||0):S=Math.max(document.documentElement.clientWidth,window.innerWidth||0),S/100*h}else return h}function ls(t,i,e,d){var m=[0,0],h=["right","left"].indexOf(d)!==-1,a=t.split(/(\+|\-)/).map(function(b){return b.trim()}),E=a.indexOf(Vn(a,function(b){return b.search(/,|\s/)!==-1}));a[E]&&a[E].indexOf(",")===-1&&console.warn("Offsets separated by white space(s) are deprecated, use a comma (,) instead.");var C=/\s*,\s*|\s+/,S=E!==-1?[a.slice(0,E).concat([a[E].split(C)[0]]),[a[E].split(C)[1]].concat(a.slice(E+1))]:[a];return S=S.map(function(b,A){var N=(A===1?!h:h)?"height":"width",O=!1;return b.reduce(function(L,M){return L[L.length-1]===""&&["+","-"].indexOf(M)!==-1?(L[L.length-1]=M,O=!0,L):O?(L[L.length-1]+=M,O=!1,L):L.concat(M)},[]).map(function(L){return ss(L,N,i,e)})}),S.forEach(function(b,A){b.forEach(function(N,O){fa(N)&&(m[A]+=N*(b[O-1]==="-"?-1:1))})}),m}function us(t,i){var e=i.offset,d=t.placement,m=t.offsets,h=m.popper,a=m.reference,E=d.split("-")[0],C=void 0;return fa(+e)?C=[+e,0]:C=ls(e,h,a,E),E==="left"?(h.top+=C[0],h.left-=C[1]):E==="right"?(h.top+=C[0],h.left+=C[1]):E==="top"?(h.left+=C[0],h.top-=C[1]):E==="bottom"&&(h.left+=C[0],h.top+=C[1]),t.popper=h,t}function cs(t,i){var e=i.boundariesElement||dn(t.instance.popper);t.instance.reference===e&&(e=dn(e));var d=da("transform"),m=t.instance.popper.style,h=m.top,a=m.left,E=m[d];m.top="",m.left="",m[d]="";var C=ca(t.instance.popper,t.instance.reference,i.padding,e,t.positionFixed);m.top=h,m.left=a,m[d]=E,i.boundaries=C;var S=i.priority,b=t.offsets.popper,A={primary:function(O){var L=b[O];return b[O]<C[O]&&!i.escapeWithReference&&(L=Math.max(b[O],C[O])),hn({},O,L)},secondary:function(O){var L=O==="right"?"left":"top",M=b[L];return b[O]>C[O]&&!i.escapeWithReference&&(M=Math.min(b[L],C[O]-(O==="right"?b.width:b.height))),hn({},L,M)}};return S.forEach(function(N){var O=["left","top"].indexOf(N)!==-1?"primary":"secondary";b=le({},b,A[O](N))}),t.offsets.popper=b,t}function ds(t){var i=t.placement,e=i.split("-")[0],d=i.split("-")[1];if(d){var m=t.offsets,h=m.reference,a=m.popper,E=["bottom","top"].indexOf(e)!==-1,C=E?"left":"top",S=E?"width":"height",b={start:hn({},C,h[C]),end:hn({},C,h[C]+h[S]-a[S])};t.offsets.popper=le({},a,b[d])}return t}function fs(t){if(!gi(t.instance.modifiers,"hide","preventOverflow"))return t;var i=t.offsets.reference,e=Vn(t.instance.modifiers,function(d){return d.name==="preventOverflow"}).boundaries;if(i.bottom<e.top||i.left>e.right||i.top>e.bottom||i.right<e.left){if(t.hide===!0)return t;t.hide=!0,t.attributes["x-out-of-boundaries"]=""}else{if(t.hide===!1)return t;t.hide=!1,t.attributes["x-out-of-boundaries"]=!1}return t}function hs(t){var i=t.placement,e=i.split("-")[0],d=t.offsets,m=d.popper,h=d.reference,a=["left","right"].indexOf(e)!==-1,E=["top","left"].indexOf(e)===-1;return m[a?"left":"top"]=h[e]-(E?m[a?"width":"height"]:0),t.placement=mt(i),t.offsets.popper=xe(m),t}var ps={shift:{order:100,enabled:!0,fn:ds},offset:{order:200,enabled:!0,fn:us,offset:0},preventOverflow:{order:300,enabled:!0,fn:cs,priority:["left","right","top","bottom"],padding:5,boundariesElement:"scrollParent"},keepTogether:{order:400,enabled:!0,fn:os},arrow:{order:500,enabled:!0,fn:as,element:"[x-arrow]"},flip:{order:600,enabled:!0,fn:rs,behavior:"flip",padding:5,boundariesElement:"viewport",flipVariations:!1,flipVariationsByContent:!1},inner:{order:700,enabled:!1,fn:hs},hide:{order:800,enabled:!0,fn:fs},computeStyle:{order:850,enabled:!0,fn:ts,gpuAcceleration:!0,x:"bottom",y:"right"},applyStyle:{order:900,enabled:!0,fn:Xo,onLoad:Zo,gpuAcceleration:void 0}},ms={placement:"bottom",positionFixed:!1,eventsEnabled:!0,removeOnDestroy:!1,onCreate:function(){},onUpdate:function(){},modifiers:ps},vt=(function(){function t(i,e){var d=this,m=arguments.length>2&&arguments[2]!==void 0?arguments[2]:{};Uo(this,t),this.scheduleUpdate=function(){return requestAnimationFrame(d.update)},this.update=Po(this.update.bind(this)),this.options=le({},t.Defaults,m),this.state={isDestroyed:!1,isCreated:!1,scrollParents:[]},this.reference=i&&i.jquery?i[0]:i,this.popper=e&&e.jquery?e[0]:e,this.options.modifiers={},Object.keys(le({},t.Defaults.modifiers,m.modifiers)).forEach(function(a){d.options.modifiers[a]=le({},t.Defaults.modifiers[a]||{},m.modifiers?m.modifiers[a]:{})}),this.modifiers=Object.keys(this.options.modifiers).map(function(a){return le({name:a},d.options.modifiers[a])}).sort(function(a,E){return a.order-E.order}),this.modifiers.forEach(function(a){a.enabled&&ai(a.onLoad)&&a.onLoad(d.reference,d.popper,d.options,a,d.state)}),this.update();var h=this.options.eventsEnabled;h&&this.enableEventListeners(),this.state.eventsEnabled=h}return Bo(t,[{key:"update",value:function(){return Vo.call(this)}},{key:"destroy",value:function(){return Wo.call(this)}},{key:"enableEventListeners",value:function(){return zo.call(this)}},{key:"disableEventListeners",value:function(){return Qo.call(this)}}]),t})();vt.Utils=(typeof window<"u"?window:global).PopperUtils;vt.placements=vi;vt.Defaults=ms;const gs=Object.freeze(Object.defineProperty({__proto__:null,default:vt},Symbol.toStringTag,{value:"Module"})),vs=Io(gs);var _s=Un.exports,Za;function Es(){return Za||(Za=1,(function(t,i){(function(e,d){d(i,Oo(),vs)})(_s,(function(e,d,m){function h(p){return p&&typeof p=="object"&&"default"in p?p:{default:p}}var a=h(d),E=h(m);function C(p,c){for(var u=0;u<c.length;u++){var n=c[u];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(p,n.key,n)}}function S(p,c,u){return u&&C(p,u),Object.defineProperty(p,"prototype",{writable:!1}),p}function b(){return b=Object.assign?Object.assign.bind():function(p){for(var c=1;c<arguments.length;c++){var u=arguments[c];for(var n in u)Object.prototype.hasOwnProperty.call(u,n)&&(p[n]=u[n])}return p},b.apply(this,arguments)}function A(p,c){p.prototype=Object.create(c.prototype),p.prototype.constructor=p,N(p,c)}function N(p,c){return N=Object.setPrototypeOf?Object.setPrototypeOf.bind():function(n,r){return n.__proto__=r,n},N(p,c)}var O="transitionend",L=1e6,M=1e3;function V(p){return p===null||typeof p>"u"?""+p:{}.toString.call(p).match(/\s([a-z]+)/i)[1].toLowerCase()}function ee(){return{bindType:O,delegateType:O,handle:function(c){if(a.default(c.target).is(this))return c.handleObj.handler.apply(this,arguments)}}}function Y(p){var c=this,u=!1;return a.default(this).one(D.TRANSITION_END,function(){u=!0}),setTimeout(function(){u||D.triggerTransitionEnd(c)},p),this}function K(){a.default.fn.emulateTransitionEnd=Y,a.default.event.special[D.TRANSITION_END]=ee()}var D={TRANSITION_END:"bsTransitionEnd",getUID:function(c){do c+=~~(Math.random()*L);while(document.getElementById(c));return c},getSelectorFromElement:function(c){var u=c.getAttribute("data-target");if(!u||u==="#"){var n=c.getAttribute("href");u=n&&n!=="#"?n.trim():""}try{return document.querySelector(u)?u:null}catch{return null}},getTransitionDurationFromElement:function(c){if(!c)return 0;var u=a.default(c).css("transition-duration"),n=a.default(c).css("transition-delay"),r=parseFloat(u),l=parseFloat(n);return!r&&!l?0:(u=u.split(",")[0],n=n.split(",")[0],(parseFloat(u)+parseFloat(n))*M)},reflow:function(c){return c.offsetHeight},triggerTransitionEnd:function(c){a.default(c).trigger(O)},supportsTransitionEnd:function(){return!!O},isElement:function(c){return(c[0]||c).nodeType},typeCheckConfig:function(c,u,n){for(var r in n)if(Object.prototype.hasOwnProperty.call(n,r)){var l=n[r],g=u[r],_=g&&D.isElement(g)?"element":V(g);if(!new RegExp(l).test(_))throw new Error(c.toUpperCase()+": "+('Option "'+r+'" provided type "'+_+'" ')+('but expected type "'+l+'".'))}},findShadowRoot:function(c){if(!document.documentElement.attachShadow)return null;if(typeof c.getRootNode=="function"){var u=c.getRootNode();return u instanceof ShadowRoot?u:null}return c instanceof ShadowRoot?c:c.parentNode?D.findShadowRoot(c.parentNode):null},jQueryDetection:function(){if(typeof a.default>"u")throw new TypeError("Bootstrap's JavaScript requires jQuery. jQuery must be included before Bootstrap's JavaScript.");var c=a.default.fn.jquery.split(" ")[0].split("."),u=1,n=2,r=9,l=1,g=4;if(c[0]<n&&c[1]<r||c[0]===u&&c[1]===r&&c[2]<l||c[0]>=g)throw new Error("Bootstrap's JavaScript requires at least jQuery v1.9.1 but less than v4.0.0")}};D.jQueryDetection(),K();var re="alert",_e="4.6.2",ue="bs.alert",ge="."+ue,mn=".data-api",ke=a.default.fn[re],_t="alert",Ve="fade",De="show",Et="close"+ge,Wn="closed"+ge,yt="click"+ge+mn,bt='[data-dismiss="alert"]',Ee=(function(){function p(u){this._element=u}var c=p.prototype;return c.close=function(n){var r=this._element;n&&(r=this._getRootElement(n));var l=this._triggerCloseEvent(r);l.isDefaultPrevented()||this._removeElement(r)},c.dispose=function(){a.default.removeData(this._element,ue),this._element=null},c._getRootElement=function(n){var r=D.getSelectorFromElement(n),l=!1;return r&&(l=document.querySelector(r)),l||(l=a.default(n).closest("."+_t)[0]),l},c._triggerCloseEvent=function(n){var r=a.default.Event(Et);return a.default(n).trigger(r),r},c._removeElement=function(n){var r=this;if(a.default(n).removeClass(De),!a.default(n).hasClass(Ve)){this._destroyElement(n);return}var l=D.getTransitionDurationFromElement(n);a.default(n).one(D.TRANSITION_END,function(g){return r._destroyElement(n,g)}).emulateTransitionEnd(l)},c._destroyElement=function(n){a.default(n).detach().trigger(Wn).remove()},p._jQueryInterface=function(n){return this.each(function(){var r=a.default(this),l=r.data(ue);l||(l=new p(this),r.data(ue,l)),n==="close"&&l[n](this)})},p._handleDismiss=function(n){return function(r){r&&r.preventDefault(),n.close(this)}},S(p,null,[{key:"VERSION",get:function(){return _e}}]),p})();a.default(document).on(yt,bt,Ee._handleDismiss(new Ee)),a.default.fn[re]=Ee._jQueryInterface,a.default.fn[re].Constructor=Ee,a.default.fn[re].noConflict=function(){return a.default.fn[re]=ke,Ee._jQueryInterface};var Se="button",Ct="4.6.2",Ae="bs.button",We="."+Ae,Ke=".data-api",wt=a.default.fn[Se],J="active",gn="btn",ze="focus",ye="click"+We+Ke,Ge="focus"+We+Ke+" "+("blur"+We+Ke),Dt="load"+We+Ke,vn='[data-toggle^="button"]',Qe='[data-toggle="buttons"]',St='[data-toggle="button"]',At='[data-toggle="buttons"] .btn',Je='input:not([type="hidden"])',Tt=".active",_n=".btn",Te=(function(){function p(u){this._element=u,this.shouldAvoidTriggerChange=!1}var c=p.prototype;return c.toggle=function(){var n=!0,r=!0,l=a.default(this._element).closest(Qe)[0];if(l){var g=this._element.querySelector(Je);if(g){if(g.type==="radio")if(g.checked&&this._element.classList.contains(J))n=!1;else{var _=l.querySelector(Tt);_&&a.default(_).removeClass(J)}n&&((g.type==="checkbox"||g.type==="radio")&&(g.checked=!this._element.classList.contains(J)),this.shouldAvoidTriggerChange||a.default(g).trigger("change")),g.focus(),r=!1}}this._element.hasAttribute("disabled")||this._element.classList.contains("disabled")||(r&&this._element.setAttribute("aria-pressed",!this._element.classList.contains(J)),n&&a.default(this._element).toggleClass(J))},c.dispose=function(){a.default.removeData(this._element,Ae),this._element=null},p._jQueryInterface=function(n,r){return this.each(function(){var l=a.default(this),g=l.data(Ae);g||(g=new p(this),l.data(Ae,g)),g.shouldAvoidTriggerChange=r,n==="toggle"&&g[n]()})},S(p,null,[{key:"VERSION",get:function(){return Ct}}]),p})();a.default(document).on(ye,vn,function(p){var c=p.target,u=c;if(a.default(c).hasClass(gn)||(c=a.default(c).closest(_n)[0]),!c||c.hasAttribute("disabled")||c.classList.contains("disabled"))p.preventDefault();else{var n=c.querySelector(Je);if(n&&(n.hasAttribute("disabled")||n.classList.contains("disabled"))){p.preventDefault();return}(u.tagName==="INPUT"||c.tagName!=="LABEL")&&Te._jQueryInterface.call(a.default(c),"toggle",u.tagName==="INPUT")}}).on(Ge,vn,function(p){var c=a.default(p.target).closest(_n)[0];a.default(c).toggleClass(ze,/^focus(in)?$/.test(p.type))}),a.default(window).on(Dt,function(){for(var p=[].slice.call(document.querySelectorAll(At)),c=0,u=p.length;c<u;c++){var n=p[c],r=n.querySelector(Je);r.checked||r.hasAttribute("checked")?n.classList.add(J):n.classList.remove(J)}p=[].slice.call(document.querySelectorAll(St));for(var l=0,g=p.length;l<g;l++){var _=p[l];_.getAttribute("aria-pressed")==="true"?_.classList.add(J):_.classList.remove(J)}}),a.default.fn[Se]=Te._jQueryInterface,a.default.fn[Se].Constructor=Te,a.default.fn[Se].noConflict=function(){return a.default.fn[Se]=wt,Te._jQueryInterface};var ce="carousel",$t="4.6.2",Le="bs.carousel",z="."+Le,Xe=".data-api",Kn=a.default.fn[ce],Ze=37,It=39,zn=500,Ot=40,Gn="carousel",be="active",Nt="slide",Qn="carousel-item-right",Mt="carousel-item-left",xt="carousel-item-next",H="carousel-item-prev",En="pointer-event",$e="next",en="prev",nn="left",yn="right",de="slide"+z,Jn="slid"+z,kt="keydown"+z,o="mouseenter"+z,s="mouseleave"+z,f="touchstart"+z,v="touchmove"+z,w="touchend"+z,T="pointerdown"+z,F="pointerup"+z,I="dragstart"+z,P="load"+z+Xe,$="click"+z+Xe,x=".active",R=".active.carousel-item",oe=".carousel-item",X=".carousel-item img",Fe=".carousel-item-next, .carousel-item-prev",Ie=".carousel-indicators",Lt="[data-slide], [data-slide-to]",bn='[data-ride="carousel"]',Cn={interval:5e3,keyboard:!0,slide:!1,pause:"hover",wrap:!0,touch:!0},Ft={interval:"(number|boolean)",keyboard:"boolean",slide:"(boolean|string)",pause:"(string|boolean)",wrap:"boolean",touch:"boolean"},Xn={TOUCH:"touch",PEN:"pen"},Oe=(function(){function p(u,n){this._items=null,this._interval=null,this._activeElement=null,this._isPaused=!1,this._isSliding=!1,this.touchTimeout=null,this.touchStartX=0,this.touchDeltaX=0,this._config=this._getConfig(n),this._element=u,this._indicatorsElement=this._element.querySelector(Ie),this._touchSupported="ontouchstart"in document.documentElement||navigator.maxTouchPoints>0,this._pointerEvent=!!(window.PointerEvent||window.MSPointerEvent),this._addEventListeners()}var c=p.prototype;return c.next=function(){this._isSliding||this._slide($e)},c.nextWhenVisible=function(){var n=a.default(this._element);!document.hidden&&n.is(":visible")&&n.css("visibility")!=="hidden"&&this.next()},c.prev=function(){this._isSliding||this._slide(en)},c.pause=function(n){n||(this._isPaused=!0),this._element.querySelector(Fe)&&(D.triggerTransitionEnd(this._element),this.cycle(!0)),clearInterval(this._interval),this._interval=null},c.cycle=function(n){n||(this._isPaused=!1),this._interval&&(clearInterval(this._interval),this._interval=null),this._config.interval&&!this._isPaused&&(this._updateInterval(),this._interval=setInterval((document.visibilityState?this.nextWhenVisible:this.next).bind(this),this._config.interval))},c.to=function(n){var r=this;this._activeElement=this._element.querySelector(R);var l=this._getItemIndex(this._activeElement);if(!(n>this._items.length-1||n<0)){if(this._isSliding){a.default(this._element).one(Jn,function(){return r.to(n)});return}if(l===n){this.pause(),this.cycle();return}var g=n>l?$e:en;this._slide(g,this._items[n])}},c.dispose=function(){a.default(this._element).off(z),a.default.removeData(this._element,Le),this._items=null,this._config=null,this._element=null,this._interval=null,this._isPaused=null,this._isSliding=null,this._activeElement=null,this._indicatorsElement=null},c._getConfig=function(n){return n=b({},Cn,n),D.typeCheckConfig(ce,n,Ft),n},c._handleSwipe=function(){var n=Math.abs(this.touchDeltaX);if(!(n<=Ot)){var r=n/this.touchDeltaX;this.touchDeltaX=0,r>0&&this.prev(),r<0&&this.next()}},c._addEventListeners=function(){var n=this;this._config.keyboard&&a.default(this._element).on(kt,function(r){return n._keydown(r)}),this._config.pause==="hover"&&a.default(this._element).on(o,function(r){return n.pause(r)}).on(s,function(r){return n.cycle(r)}),this._config.touch&&this._addTouchEventListeners()},c._addTouchEventListeners=function(){var n=this;if(this._touchSupported){var r=function(y){n._pointerEvent&&Xn[y.originalEvent.pointerType.toUpperCase()]?n.touchStartX=y.originalEvent.clientX:n._pointerEvent||(n.touchStartX=y.originalEvent.touches[0].clientX)},l=function(y){n.touchDeltaX=y.originalEvent.touches&&y.originalEvent.touches.length>1?0:y.originalEvent.touches[0].clientX-n.touchStartX},g=function(y){n._pointerEvent&&Xn[y.originalEvent.pointerType.toUpperCase()]&&(n.touchDeltaX=y.originalEvent.clientX-n.touchStartX),n._handleSwipe(),n._config.pause==="hover"&&(n.pause(),n.touchTimeout&&clearTimeout(n.touchTimeout),n.touchTimeout=setTimeout(function(k){return n.cycle(k)},zn+n._config.interval))};a.default(this._element.querySelectorAll(X)).on(I,function(_){return _.preventDefault()}),this._pointerEvent?(a.default(this._element).on(T,function(_){return r(_)}),a.default(this._element).on(F,function(_){return g(_)}),this._element.classList.add(En)):(a.default(this._element).on(f,function(_){return r(_)}),a.default(this._element).on(v,function(_){return l(_)}),a.default(this._element).on(w,function(_){return g(_)}))}},c._keydown=function(n){if(!/input|textarea/i.test(n.target.tagName))switch(n.which){case Ze:n.preventDefault(),this.prev();break;case It:n.preventDefault(),this.next();break}},c._getItemIndex=function(n){return this._items=n&&n.parentNode?[].slice.call(n.parentNode.querySelectorAll(oe)):[],this._items.indexOf(n)},c._getItemByDirection=function(n,r){var l=n===$e,g=n===en,_=this._getItemIndex(r),y=this._items.length-1,k=g&&_===0||l&&_===y;if(k&&!this._config.wrap)return r;var j=n===en?-1:1,U=(_+j)%this._items.length;return U===-1?this._items[this._items.length-1]:this._items[U]},c._triggerSlideEvent=function(n,r){var l=this._getItemIndex(n),g=this._getItemIndex(this._element.querySelector(R)),_=a.default.Event(de,{relatedTarget:n,direction:r,from:g,to:l});return a.default(this._element).trigger(_),_},c._setActiveIndicatorElement=function(n){if(this._indicatorsElement){var r=[].slice.call(this._indicatorsElement.querySelectorAll(x));a.default(r).removeClass(be);var l=this._indicatorsElement.children[this._getItemIndex(n)];l&&a.default(l).addClass(be)}},c._updateInterval=function(){var n=this._activeElement||this._element.querySelector(R);if(n){var r=parseInt(n.getAttribute("data-interval"),10);r?(this._config.defaultInterval=this._config.defaultInterval||this._config.interval,this._config.interval=r):this._config.interval=this._config.defaultInterval||this._config.interval}},c._slide=function(n,r){var l=this,g=this._element.querySelector(R),_=this._getItemIndex(g),y=r||g&&this._getItemByDirection(n,g),k=this._getItemIndex(y),j=!!this._interval,U,W,ve;if(n===$e?(U=Mt,W=xt,ve=nn):(U=Qn,W=H,ve=yn),y&&a.default(y).hasClass(be)){this._isSliding=!1;return}var me=this._triggerSlideEvent(y,ve);if(!me.isDefaultPrevented()&&!(!g||!y)){this._isSliding=!0,j&&this.pause(),this._setActiveIndicatorElement(y),this._activeElement=y;var ln=a.default.Event(Jn,{relatedTarget:y,direction:ve,from:_,to:k});if(a.default(this._element).hasClass(Nt)){a.default(y).addClass(W),D.reflow(y),a.default(g).addClass(U),a.default(y).addClass(U);var Qt=D.getTransitionDurationFromElement(g);a.default(g).one(D.TRANSITION_END,function(){a.default(y).removeClass(U+" "+W).addClass(be),a.default(g).removeClass(be+" "+W+" "+U),l._isSliding=!1,setTimeout(function(){return a.default(l._element).trigger(ln)},0)}).emulateTransitionEnd(Qt)}else a.default(g).removeClass(be),a.default(y).addClass(be),this._isSliding=!1,a.default(this._element).trigger(ln);j&&this.cycle()}},p._jQueryInterface=function(n){return this.each(function(){var r=a.default(this).data(Le),l=b({},Cn,a.default(this).data());typeof n=="object"&&(l=b({},l,n));var g=typeof n=="string"?n:l.slide;if(r||(r=new p(this,l),a.default(this).data(Le,r)),typeof n=="number")r.to(n);else if(typeof g=="string"){if(typeof r[g]>"u")throw new TypeError('No method named "'+g+'"');r[g]()}else l.interval&&l.ride&&(r.pause(),r.cycle())})},p._dataApiClickHandler=function(n){var r=D.getSelectorFromElement(this);if(r){var l=a.default(r)[0];if(!(!l||!a.default(l).hasClass(Gn))){var g=b({},a.default(l).data(),a.default(this).data()),_=this.getAttribute("data-slide-to");_&&(g.interval=!1),p._jQueryInterface.call(a.default(l),g),_&&a.default(l).data(Le).to(_),n.preventDefault()}}},S(p,null,[{key:"VERSION",get:function(){return $t}},{key:"Default",get:function(){return Cn}}]),p})();a.default(document).on($,Lt,Oe._dataApiClickHandler),a.default(window).on(P,function(){for(var p=[].slice.call(document.querySelectorAll(bn)),c=0,u=p.length;c<u;c++){var n=a.default(p[c]);Oe._jQueryInterface.call(n,n.data())}}),a.default.fn[ce]=Oe._jQueryInterface,a.default.fn[ce].Constructor=Oe,a.default.fn[ce].noConflict=function(){return a.default.fn[ce]=Kn,Oe._jQueryInterface};var Ne="collapse",Pt="4.6.2",Ce="bs.collapse",Pe="."+Ce,yi=".data-api",bi=a.default.fn[Ne],Re="show",wn="collapse",Zn="collapsing",Rt="collapsed",ha="width",Ci="height",wi="show"+Pe,Di="shown"+Pe,Si="hide"+Pe,Ai="hidden"+Pe,Ti="click"+Pe+yi,$i=".show, .collapsing",pa='[data-toggle="collapse"]',jt={toggle:!0,parent:""},Ii={toggle:"boolean",parent:"(string|element)"},Dn=(function(){function p(u,n){this._isTransitioning=!1,this._element=u,this._config=this._getConfig(n),this._triggerArray=[].slice.call(document.querySelectorAll('[data-toggle="collapse"][href="#'+u.id+'"],'+('[data-toggle="collapse"][data-target="#'+u.id+'"]')));for(var r=[].slice.call(document.querySelectorAll(pa)),l=0,g=r.length;l<g;l++){var _=r[l],y=D.getSelectorFromElement(_),k=[].slice.call(document.querySelectorAll(y)).filter(function(j){return j===u});y!==null&&k.length>0&&(this._selector=y,this._triggerArray.push(_))}this._parent=this._config.parent?this._getParent():null,this._config.parent||this._addAriaAndCollapsedClass(this._element,this._triggerArray),this._config.toggle&&this.toggle()}var c=p.prototype;return c.toggle=function(){a.default(this._element).hasClass(Re)?this.hide():this.show()},c.show=function(){var n=this;if(!(this._isTransitioning||a.default(this._element).hasClass(Re))){var r,l;if(this._parent&&(r=[].slice.call(this._parent.querySelectorAll($i)).filter(function(W){return typeof n._config.parent=="string"?W.getAttribute("data-parent")===n._config.parent:W.classList.contains(wn)}),r.length===0&&(r=null)),!(r&&(l=a.default(r).not(this._selector).data(Ce),l&&l._isTransitioning))){var g=a.default.Event(wi);if(a.default(this._element).trigger(g),!g.isDefaultPrevented()){r&&(p._jQueryInterface.call(a.default(r).not(this._selector),"hide"),l||a.default(r).data(Ce,null));var _=this._getDimension();a.default(this._element).removeClass(wn).addClass(Zn),this._element.style[_]=0,this._triggerArray.length&&a.default(this._triggerArray).removeClass(Rt).attr("aria-expanded",!0),this.setTransitioning(!0);var y=function(){a.default(n._element).removeClass(Zn).addClass(wn+" "+Re),n._element.style[_]="",n.setTransitioning(!1),a.default(n._element).trigger(Di)},k=_[0].toUpperCase()+_.slice(1),j="scroll"+k,U=D.getTransitionDurationFromElement(this._element);a.default(this._element).one(D.TRANSITION_END,y).emulateTransitionEnd(U),this._element.style[_]=this._element[j]+"px"}}}},c.hide=function(){var n=this;if(!(this._isTransitioning||!a.default(this._element).hasClass(Re))){var r=a.default.Event(Si);if(a.default(this._element).trigger(r),!r.isDefaultPrevented()){var l=this._getDimension();this._element.style[l]=this._element.getBoundingClientRect()[l]+"px",D.reflow(this._element),a.default(this._element).addClass(Zn).removeClass(wn+" "+Re);var g=this._triggerArray.length;if(g>0)for(var _=0;_<g;_++){var y=this._triggerArray[_],k=D.getSelectorFromElement(y);if(k!==null){var j=a.default([].slice.call(document.querySelectorAll(k)));j.hasClass(Re)||a.default(y).addClass(Rt).attr("aria-expanded",!1)}}this.setTransitioning(!0);var U=function(){n.setTransitioning(!1),a.default(n._element).removeClass(Zn).addClass(wn).trigger(Ai)};this._element.style[l]="";var W=D.getTransitionDurationFromElement(this._element);a.default(this._element).one(D.TRANSITION_END,U).emulateTransitionEnd(W)}}},c.setTransitioning=function(n){this._isTransitioning=n},c.dispose=function(){a.default.removeData(this._element,Ce),this._config=null,this._parent=null,this._element=null,this._triggerArray=null,this._isTransitioning=null},c._getConfig=function(n){return n=b({},jt,n),n.toggle=!!n.toggle,D.typeCheckConfig(Ne,n,Ii),n},c._getDimension=function(){var n=a.default(this._element).hasClass(ha);return n?ha:Ci},c._getParent=function(){var n=this,r;D.isElement(this._config.parent)?(r=this._config.parent,typeof this._config.parent.jquery<"u"&&(r=this._config.parent[0])):r=document.querySelector(this._config.parent);var l='[data-toggle="collapse"][data-parent="'+this._config.parent+'"]',g=[].slice.call(r.querySelectorAll(l));return a.default(g).each(function(_,y){n._addAriaAndCollapsedClass(p._getTargetFromElement(y),[y])}),r},c._addAriaAndCollapsedClass=function(n,r){var l=a.default(n).hasClass(Re);r.length&&a.default(r).toggleClass(Rt,!l).attr("aria-expanded",l)},p._getTargetFromElement=function(n){var r=D.getSelectorFromElement(n);return r?document.querySelector(r):null},p._jQueryInterface=function(n){return this.each(function(){var r=a.default(this),l=r.data(Ce),g=b({},jt,r.data(),typeof n=="object"&&n?n:{});if(!l&&g.toggle&&typeof n=="string"&&/show|hide/.test(n)&&(g.toggle=!1),l||(l=new p(this,g),r.data(Ce,l)),typeof n=="string"){if(typeof l[n]>"u")throw new TypeError('No method named "'+n+'"');l[n]()}})},S(p,null,[{key:"VERSION",get:function(){return Pt}},{key:"Default",get:function(){return jt}}]),p})();a.default(document).on(Ti,pa,function(p){p.currentTarget.tagName==="A"&&p.preventDefault();var c=a.default(this),u=D.getSelectorFromElement(this),n=[].slice.call(document.querySelectorAll(u));a.default(n).each(function(){var r=a.default(this),l=r.data(Ce),g=l?"toggle":c.data();Dn._jQueryInterface.call(r,g)})}),a.default.fn[Ne]=Dn._jQueryInterface,a.default.fn[Ne].Constructor=Dn,a.default.fn[Ne].noConflict=function(){return a.default.fn[Ne]=bi,Dn._jQueryInterface};var tn="dropdown",Oi="4.6.2",Sn="bs.dropdown",we="."+Sn,Ut=".data-api",Ni=a.default.fn[tn],An=27,ma=32,ga=9,Bt=38,Ht=40,Mi=3,xi=new RegExp(Bt+"|"+Ht+"|"+An),et="disabled",fe="show",ki="dropup",Li="dropright",Fi="dropleft",va="dropdown-menu-right",Pi="position-static",_a="hide"+we,Ea="hidden"+we,Ri="show"+we,ji="shown"+we,Ui="click"+we,Yt="click"+we+Ut,ya="keydown"+we+Ut,Bi="keyup"+we+Ut,nt='[data-toggle="dropdown"]',Hi=".dropdown form",qt=".dropdown-menu",Yi=".navbar-nav",qi=".dropdown-menu .dropdown-item:not(.disabled):not(:disabled)",Vi="top-start",Wi="top-end",Ki="bottom-start",zi="bottom-end",Gi="right-start",Qi="left-start",Ji={offset:0,flip:!0,boundary:"scrollParent",reference:"toggle",display:"dynamic",popperConfig:null},Xi={offset:"(number|string|function)",flip:"boolean",boundary:"(string|element)",reference:"(string|element)",display:"string",popperConfig:"(null|object)"},Me=(function(){function p(u,n){this._element=u,this._popper=null,this._config=this._getConfig(n),this._menu=this._getMenuElement(),this._inNavbar=this._detectNavbar(),this._addEventListeners()}var c=p.prototype;return c.toggle=function(){if(!(this._element.disabled||a.default(this._element).hasClass(et))){var n=a.default(this._menu).hasClass(fe);p._clearMenus(),!n&&this.show(!0)}},c.show=function(n){if(n===void 0&&(n=!1),!(this._element.disabled||a.default(this._element).hasClass(et)||a.default(this._menu).hasClass(fe))){var r={relatedTarget:this._element},l=a.default.Event(Ri,r),g=p._getParentFromElement(this._element);if(a.default(g).trigger(l),!l.isDefaultPrevented()){if(!this._inNavbar&&n){if(typeof E.default>"u")throw new TypeError("Bootstrap's dropdowns require Popper (https://popper.js.org)");var _=this._element;this._config.reference==="parent"?_=g:D.isElement(this._config.reference)&&(_=this._config.reference,typeof this._config.reference.jquery<"u"&&(_=this._config.reference[0])),this._config.boundary!=="scrollParent"&&a.default(g).addClass(Pi),this._popper=new E.default(_,this._menu,this._getPopperConfig())}"ontouchstart"in document.documentElement&&a.default(g).closest(Yi).length===0&&a.default(document.body).children().on("mouseover",null,a.default.noop),this._element.focus(),this._element.setAttribute("aria-expanded",!0),a.default(this._menu).toggleClass(fe),a.default(g).toggleClass(fe).trigger(a.default.Event(ji,r))}}},c.hide=function(){if(!(this._element.disabled||a.default(this._element).hasClass(et)||!a.default(this._menu).hasClass(fe))){var n={relatedTarget:this._element},r=a.default.Event(_a,n),l=p._getParentFromElement(this._element);a.default(l).trigger(r),!r.isDefaultPrevented()&&(this._popper&&this._popper.destroy(),a.default(this._menu).toggleClass(fe),a.default(l).toggleClass(fe).trigger(a.default.Event(Ea,n)))}},c.dispose=function(){a.default.removeData(this._element,Sn),a.default(this._element).off(we),this._element=null,this._menu=null,this._popper!==null&&(this._popper.destroy(),this._popper=null)},c.update=function(){this._inNavbar=this._detectNavbar(),this._popper!==null&&this._popper.scheduleUpdate()},c._addEventListeners=function(){var n=this;a.default(this._element).on(Ui,function(r){r.preventDefault(),r.stopPropagation(),n.toggle()})},c._getConfig=function(n){return n=b({},this.constructor.Default,a.default(this._element).data(),n),D.typeCheckConfig(tn,n,this.constructor.DefaultType),n},c._getMenuElement=function(){if(!this._menu){var n=p._getParentFromElement(this._element);n&&(this._menu=n.querySelector(qt))}return this._menu},c._getPlacement=function(){var n=a.default(this._element.parentNode),r=Ki;return n.hasClass(ki)?r=a.default(this._menu).hasClass(va)?Wi:Vi:n.hasClass(Li)?r=Gi:n.hasClass(Fi)?r=Qi:a.default(this._menu).hasClass(va)&&(r=zi),r},c._detectNavbar=function(){return a.default(this._element).closest(".navbar").length>0},c._getOffset=function(){var n=this,r={};return typeof this._config.offset=="function"?r.fn=function(l){return l.offsets=b({},l.offsets,n._config.offset(l.offsets,n._element)),l}:r.offset=this._config.offset,r},c._getPopperConfig=function(){var n={placement:this._getPlacement(),modifiers:{offset:this._getOffset(),flip:{enabled:this._config.flip},preventOverflow:{boundariesElement:this._config.boundary}}};return this._config.display==="static"&&(n.modifiers.applyStyle={enabled:!1}),b({},n,this._config.popperConfig)},p._jQueryInterface=function(n){return this.each(function(){var r=a.default(this).data(Sn),l=typeof n=="object"?n:null;if(r||(r=new p(this,l),a.default(this).data(Sn,r)),typeof n=="string"){if(typeof r[n]>"u")throw new TypeError('No method named "'+n+'"');r[n]()}})},p._clearMenus=function(n){if(!(n&&(n.which===Mi||n.type==="keyup"&&n.which!==ga)))for(var r=[].slice.call(document.querySelectorAll(nt)),l=0,g=r.length;l<g;l++){var _=p._getParentFromElement(r[l]),y=a.default(r[l]).data(Sn),k={relatedTarget:r[l]};if(n&&n.type==="click"&&(k.clickEvent=n),!!y){var j=y._menu;if(a.default(_).hasClass(fe)&&!(n&&(n.type==="click"&&/input|textarea/i.test(n.target.tagName)||n.type==="keyup"&&n.which===ga)&&a.default.contains(_,n.target))){var U=a.default.Event(_a,k);a.default(_).trigger(U),!U.isDefaultPrevented()&&("ontouchstart"in document.documentElement&&a.default(document.body).children().off("mouseover",null,a.default.noop),r[l].setAttribute("aria-expanded","false"),y._popper&&y._popper.destroy(),a.default(j).removeClass(fe),a.default(_).removeClass(fe).trigger(a.default.Event(Ea,k)))}}}},p._getParentFromElement=function(n){var r,l=D.getSelectorFromElement(n);return l&&(r=document.querySelector(l)),r||n.parentNode},p._dataApiKeydownHandler=function(n){if(!(/input|textarea/i.test(n.target.tagName)?n.which===ma||n.which!==An&&(n.which!==Ht&&n.which!==Bt||a.default(n.target).closest(qt).length):!xi.test(n.which))&&!(this.disabled||a.default(this).hasClass(et))){var r=p._getParentFromElement(this),l=a.default(r).hasClass(fe);if(!(!l&&n.which===An)){if(n.preventDefault(),n.stopPropagation(),!l||n.which===An||n.which===ma){n.which===An&&a.default(r.querySelector(nt)).trigger("focus"),a.default(this).trigger("click");return}var g=[].slice.call(r.querySelectorAll(qi)).filter(function(y){return a.default(y).is(":visible")});if(g.length!==0){var _=g.indexOf(n.target);n.which===Bt&&_>0&&_--,n.which===Ht&&_<g.length-1&&_++,_<0&&(_=0),g[_].focus()}}}},S(p,null,[{key:"VERSION",get:function(){return Oi}},{key:"Default",get:function(){return Ji}},{key:"DefaultType",get:function(){return Xi}}]),p})();a.default(document).on(ya,nt,Me._dataApiKeydownHandler).on(ya,qt,Me._dataApiKeydownHandler).on(Yt+" "+Bi,Me._clearMenus).on(Yt,nt,function(p){p.preventDefault(),p.stopPropagation(),Me._jQueryInterface.call(a.default(this),"toggle")}).on(Yt,Hi,function(p){p.stopPropagation()}),a.default.fn[tn]=Me._jQueryInterface,a.default.fn[tn].Constructor=Me,a.default.fn[tn].noConflict=function(){return a.default.fn[tn]=Ni,Me._jQueryInterface};var an="modal",Zi="4.6.2",Tn="bs.modal",te="."+Tn,er=".data-api",nr=a.default.fn[an],ba=27,tr="modal-dialog-scrollable",ar="modal-scrollbar-measure",ir="modal-backdrop",Ca="modal-open",rn="fade",tt="show",wa="modal-static",rr="hide"+te,or="hidePrevented"+te,Da="hidden"+te,Sa="show"+te,sr="shown"+te,at="focusin"+te,Aa="resize"+te,Vt="click.dismiss"+te,Ta="keydown.dismiss"+te,lr="mouseup.dismiss"+te,$a="mousedown.dismiss"+te,ur="click"+te+er,cr=".modal-dialog",dr=".modal-body",fr='[data-toggle="modal"]',hr='[data-dismiss="modal"]',Ia=".fixed-top, .fixed-bottom, .is-fixed, .sticky-top",Oa=".sticky-top",Wt={backdrop:!0,keyboard:!0,focus:!0,show:!0},pr={backdrop:"(boolean|string)",keyboard:"boolean",focus:"boolean",show:"boolean"},$n=(function(){function p(u,n){this._config=this._getConfig(n),this._element=u,this._dialog=u.querySelector(cr),this._backdrop=null,this._isShown=!1,this._isBodyOverflowing=!1,this._ignoreBackdropClick=!1,this._isTransitioning=!1,this._scrollbarWidth=0}var c=p.prototype;return c.toggle=function(n){return this._isShown?this.hide():this.show(n)},c.show=function(n){var r=this;if(!(this._isShown||this._isTransitioning)){var l=a.default.Event(Sa,{relatedTarget:n});a.default(this._element).trigger(l),!l.isDefaultPrevented()&&(this._isShown=!0,a.default(this._element).hasClass(rn)&&(this._isTransitioning=!0),this._checkScrollbar(),this._setScrollbar(),this._adjustDialog(),this._setEscapeEvent(),this._setResizeEvent(),a.default(this._element).on(Vt,hr,function(g){return r.hide(g)}),a.default(this._dialog).on($a,function(){a.default(r._element).one(lr,function(g){a.default(g.target).is(r._element)&&(r._ignoreBackdropClick=!0)})}),this._showBackdrop(function(){return r._showElement(n)}))}},c.hide=function(n){var r=this;if(n&&n.preventDefault(),!(!this._isShown||this._isTransitioning)){var l=a.default.Event(rr);if(a.default(this._element).trigger(l),!(!this._isShown||l.isDefaultPrevented())){this._isShown=!1;var g=a.default(this._element).hasClass(rn);if(g&&(this._isTransitioning=!0),this._setEscapeEvent(),this._setResizeEvent(),a.default(document).off(at),a.default(this._element).removeClass(tt),a.default(this._element).off(Vt),a.default(this._dialog).off($a),g){var _=D.getTransitionDurationFromElement(this._element);a.default(this._element).one(D.TRANSITION_END,function(y){return r._hideModal(y)}).emulateTransitionEnd(_)}else this._hideModal()}}},c.dispose=function(){[window,this._element,this._dialog].forEach(function(n){return a.default(n).off(te)}),a.default(document).off(at),a.default.removeData(this._element,Tn),this._config=null,this._element=null,this._dialog=null,this._backdrop=null,this._isShown=null,this._isBodyOverflowing=null,this._ignoreBackdropClick=null,this._isTransitioning=null,this._scrollbarWidth=null},c.handleUpdate=function(){this._adjustDialog()},c._getConfig=function(n){return n=b({},Wt,n),D.typeCheckConfig(an,n,pr),n},c._triggerBackdropTransition=function(){var n=this,r=a.default.Event(or);if(a.default(this._element).trigger(r),!r.isDefaultPrevented()){var l=this._element.scrollHeight>document.documentElement.clientHeight;l||(this._element.style.overflowY="hidden"),this._element.classList.add(wa);var g=D.getTransitionDurationFromElement(this._dialog);a.default(this._element).off(D.TRANSITION_END),a.default(this._element).one(D.TRANSITION_END,function(){n._element.classList.remove(wa),l||a.default(n._element).one(D.TRANSITION_END,function(){n._element.style.overflowY=""}).emulateTransitionEnd(n._element,g)}).emulateTransitionEnd(g),this._element.focus()}},c._showElement=function(n){var r=this,l=a.default(this._element).hasClass(rn),g=this._dialog?this._dialog.querySelector(dr):null;(!this._element.parentNode||this._element.parentNode.nodeType!==Node.ELEMENT_NODE)&&document.body.appendChild(this._element),this._element.style.display="block",this._element.removeAttribute("aria-hidden"),this._element.setAttribute("aria-modal",!0),this._element.setAttribute("role","dialog"),a.default(this._dialog).hasClass(tr)&&g?g.scrollTop=0:this._element.scrollTop=0,l&&D.reflow(this._element),a.default(this._element).addClass(tt),this._config.focus&&this._enforceFocus();var _=a.default.Event(sr,{relatedTarget:n}),y=function(){r._config.focus&&r._element.focus(),r._isTransitioning=!1,a.default(r._element).trigger(_)};if(l){var k=D.getTransitionDurationFromElement(this._dialog);a.default(this._dialog).one(D.TRANSITION_END,y).emulateTransitionEnd(k)}else y()},c._enforceFocus=function(){var n=this;a.default(document).off(at).on(at,function(r){document!==r.target&&n._element!==r.target&&a.default(n._element).has(r.target).length===0&&n._element.focus()})},c._setEscapeEvent=function(){var n=this;this._isShown?a.default(this._element).on(Ta,function(r){n._config.keyboard&&r.which===ba?(r.preventDefault(),n.hide()):!n._config.keyboard&&r.which===ba&&n._triggerBackdropTransition()}):this._isShown||a.default(this._element).off(Ta)},c._setResizeEvent=function(){var n=this;this._isShown?a.default(window).on(Aa,function(r){return n.handleUpdate(r)}):a.default(window).off(Aa)},c._hideModal=function(){var n=this;this._element.style.display="none",this._element.setAttribute("aria-hidden",!0),this._element.removeAttribute("aria-modal"),this._element.removeAttribute("role"),this._isTransitioning=!1,this._showBackdrop(function(){a.default(document.body).removeClass(Ca),n._resetAdjustments(),n._resetScrollbar(),a.default(n._element).trigger(Da)})},c._removeBackdrop=function(){this._backdrop&&(a.default(this._backdrop).remove(),this._backdrop=null)},c._showBackdrop=function(n){var r=this,l=a.default(this._element).hasClass(rn)?rn:"";if(this._isShown&&this._config.backdrop){if(this._backdrop=document.createElement("div"),this._backdrop.className=ir,l&&this._backdrop.classList.add(l),a.default(this._backdrop).appendTo(document.body),a.default(this._element).on(Vt,function(k){if(r._ignoreBackdropClick){r._ignoreBackdropClick=!1;return}k.target===k.currentTarget&&(r._config.backdrop==="static"?r._triggerBackdropTransition():r.hide())}),l&&D.reflow(this._backdrop),a.default(this._backdrop).addClass(tt),!n)return;if(!l){n();return}var g=D.getTransitionDurationFromElement(this._backdrop);a.default(this._backdrop).one(D.TRANSITION_END,n).emulateTransitionEnd(g)}else if(!this._isShown&&this._backdrop){a.default(this._backdrop).removeClass(tt);var _=function(){r._removeBackdrop(),n&&n()};if(a.default(this._element).hasClass(rn)){var y=D.getTransitionDurationFromElement(this._backdrop);a.default(this._backdrop).one(D.TRANSITION_END,_).emulateTransitionEnd(y)}else _()}else n&&n()},c._adjustDialog=function(){var n=this._element.scrollHeight>document.documentElement.clientHeight;!this._isBodyOverflowing&&n&&(this._element.style.paddingLeft=this._scrollbarWidth+"px"),this._isBodyOverflowing&&!n&&(this._element.style.paddingRight=this._scrollbarWidth+"px")},c._resetAdjustments=function(){this._element.style.paddingLeft="",this._element.style.paddingRight=""},c._checkScrollbar=function(){var n=document.body.getBoundingClientRect();this._isBodyOverflowing=Math.round(n.left+n.right)<window.innerWidth,this._scrollbarWidth=this._getScrollbarWidth()},c._setScrollbar=function(){var n=this;if(this._isBodyOverflowing){var r=[].slice.call(document.querySelectorAll(Ia)),l=[].slice.call(document.querySelectorAll(Oa));a.default(r).each(function(y,k){var j=k.style.paddingRight,U=a.default(k).css("padding-right");a.default(k).data("padding-right",j).css("padding-right",parseFloat(U)+n._scrollbarWidth+"px")}),a.default(l).each(function(y,k){var j=k.style.marginRight,U=a.default(k).css("margin-right");a.default(k).data("margin-right",j).css("margin-right",parseFloat(U)-n._scrollbarWidth+"px")});var g=document.body.style.paddingRight,_=a.default(document.body).css("padding-right");a.default(document.body).data("padding-right",g).css("padding-right",parseFloat(_)+this._scrollbarWidth+"px")}a.default(document.body).addClass(Ca)},c._resetScrollbar=function(){var n=[].slice.call(document.querySelectorAll(Ia));a.default(n).each(function(g,_){var y=a.default(_).data("padding-right");a.default(_).removeData("padding-right"),_.style.paddingRight=y||""});var r=[].slice.call(document.querySelectorAll(""+Oa));a.default(r).each(function(g,_){var y=a.default(_).data("margin-right");typeof y<"u"&&a.default(_).css("margin-right",y).removeData("margin-right")});var l=a.default(document.body).data("padding-right");a.default(document.body).removeData("padding-right"),document.body.style.paddingRight=l||""},c._getScrollbarWidth=function(){var n=document.createElement("div");n.className=ar,document.body.appendChild(n);var r=n.getBoundingClientRect().width-n.clientWidth;return document.body.removeChild(n),r},p._jQueryInterface=function(n,r){return this.each(function(){var l=a.default(this).data(Tn),g=b({},Wt,a.default(this).data(),typeof n=="object"&&n?n:{});if(l||(l=new p(this,g),a.default(this).data(Tn,l)),typeof n=="string"){if(typeof l[n]>"u")throw new TypeError('No method named "'+n+'"');l[n](r)}else g.show&&l.show(r)})},S(p,null,[{key:"VERSION",get:function(){return Zi}},{key:"Default",get:function(){return Wt}}]),p})();a.default(document).on(ur,fr,function(p){var c=this,u,n=D.getSelectorFromElement(this);n&&(u=document.querySelector(n));var r=a.default(u).data(Tn)?"toggle":b({},a.default(u).data(),a.default(this).data());(this.tagName==="A"||this.tagName==="AREA")&&p.preventDefault();var l=a.default(u).one(Sa,function(g){g.isDefaultPrevented()||l.one(Da,function(){a.default(c).is(":visible")&&c.focus()})});$n._jQueryInterface.call(a.default(u),r,this)}),a.default.fn[an]=$n._jQueryInterface,a.default.fn[an].Constructor=$n,a.default.fn[an].noConflict=function(){return a.default.fn[an]=nr,$n._jQueryInterface};var mr=["background","cite","href","itemtype","longdesc","poster","src","xlink:href"],gr=/^aria-[\w-]*$/i,vr={"*":["class","dir","id","lang","role",gr],a:["target","href","title","rel"],area:[],b:[],br:[],col:[],code:[],div:[],em:[],hr:[],h1:[],h2:[],h3:[],h4:[],h5:[],h6:[],i:[],img:["src","srcset","alt","title","width","height"],li:[],ol:[],p:[],pre:[],s:[],small:[],span:[],sub:[],sup:[],strong:[],u:[],ul:[]},_r=/^(?:(?:https?|mailto|ftp|tel|file|sms):|[^#&/:?]*(?:[#/?]|$))/i,Er=/^data:(?:image\/(?:bmp|gif|jpeg|jpg|png|tiff|webp)|video\/(?:mpeg|mp4|ogg|webm)|audio\/(?:mp3|oga|ogg|opus));base64,[\d+/a-z]+=*$/i;function yr(p,c){var u=p.nodeName.toLowerCase();if(c.indexOf(u)!==-1)return mr.indexOf(u)!==-1?!!(_r.test(p.nodeValue)||Er.test(p.nodeValue)):!0;for(var n=c.filter(function(g){return g instanceof RegExp}),r=0,l=n.length;r<l;r++)if(n[r].test(u))return!0;return!1}function Na(p,c,u){if(p.length===0)return p;if(u&&typeof u=="function")return u(p);for(var n=new window.DOMParser,r=n.parseFromString(p,"text/html"),l=Object.keys(c),g=[].slice.call(r.body.querySelectorAll("*")),_=function(W,ve){var me=g[W],ln=me.nodeName.toLowerCase();if(l.indexOf(me.nodeName.toLowerCase())===-1)return me.parentNode.removeChild(me),"continue";var Qt=[].slice.call(me.attributes),$o=[].concat(c["*"]||[],c[ln]||[]);Qt.forEach(function(Wa){yr(Wa,$o)||me.removeAttribute(Wa.nodeName)})},y=0,k=g.length;y<k;y++)var j=_(y);return r.body.innerHTML}var je="tooltip",br="4.6.2",it="bs.tooltip",he="."+it,Cr=a.default.fn[je],Ma="bs-tooltip",wr=new RegExp("(^|\\s)"+Ma+"\\S+","g"),Dr=["sanitize","whiteList","sanitizeFn"],In="fade",On="show",Nn="show",Kt="out",Sr=".tooltip-inner",Ar=".arrow",Mn="hover",zt="focus",Tr="click",$r="manual",Ir={AUTO:"auto",TOP:"top",RIGHT:"right",BOTTOM:"bottom",LEFT:"left"},Or={animation:!0,template:'<div class="tooltip" role="tooltip"><div class="arrow"></div><div class="tooltip-inner"></div></div>',trigger:"hover focus",title:"",delay:0,html:!1,selector:!1,placement:"top",offset:0,container:!1,fallbackPlacement:"flip",boundary:"scrollParent",customClass:"",sanitize:!0,sanitizeFn:null,whiteList:vr,popperConfig:null},Nr={animation:"boolean",template:"string",title:"(string|element|function)",trigger:"string",delay:"(number|object)",html:"boolean",selector:"(string|boolean)",placement:"(string|function)",offset:"(number|string|function)",container:"(string|element|boolean)",fallbackPlacement:"(string|array)",boundary:"(string|element)",customClass:"(string|function)",sanitize:"boolean",sanitizeFn:"(null|function)",whiteList:"object",popperConfig:"(null|object)"},Mr={HIDE:"hide"+he,HIDDEN:"hidden"+he,SHOW:"show"+he,SHOWN:"shown"+he,INSERTED:"inserted"+he,CLICK:"click"+he,FOCUSIN:"focusin"+he,FOCUSOUT:"focusout"+he,MOUSEENTER:"mouseenter"+he,MOUSELEAVE:"mouseleave"+he},Ue=(function(){function p(u,n){if(typeof E.default>"u")throw new TypeError("Bootstrap's tooltips require Popper (https://popper.js.org)");this._isEnabled=!0,this._timeout=0,this._hoverState="",this._activeTrigger={},this._popper=null,this.element=u,this.config=this._getConfig(n),this.tip=null,this._setListeners()}var c=p.prototype;return c.enable=function(){this._isEnabled=!0},c.disable=function(){this._isEnabled=!1},c.toggleEnabled=function(){this._isEnabled=!this._isEnabled},c.toggle=function(n){if(this._isEnabled)if(n){var r=this.constructor.DATA_KEY,l=a.default(n.currentTarget).data(r);l||(l=new this.constructor(n.currentTarget,this._getDelegateConfig()),a.default(n.currentTarget).data(r,l)),l._activeTrigger.click=!l._activeTrigger.click,l._isWithActiveTrigger()?l._enter(null,l):l._leave(null,l)}else{if(a.default(this.getTipElement()).hasClass(On)){this._leave(null,this);return}this._enter(null,this)}},c.dispose=function(){clearTimeout(this._timeout),a.default.removeData(this.element,this.constructor.DATA_KEY),a.default(this.element).off(this.constructor.EVENT_KEY),a.default(this.element).closest(".modal").off("hide.bs.modal",this._hideModalHandler),this.tip&&a.default(this.tip).remove(),this._isEnabled=null,this._timeout=null,this._hoverState=null,this._activeTrigger=null,this._popper&&this._popper.destroy(),this._popper=null,this.element=null,this.config=null,this.tip=null},c.show=function(){var n=this;if(a.default(this.element).css("display")==="none")throw new Error("Please use show on visible elements");var r=a.default.Event(this.constructor.Event.SHOW);if(this.isWithContent()&&this._isEnabled){a.default(this.element).trigger(r);var l=D.findShadowRoot(this.element),g=a.default.contains(l!==null?l:this.element.ownerDocument.documentElement,this.element);if(r.isDefaultPrevented()||!g)return;var _=this.getTipElement(),y=D.getUID(this.constructor.NAME);_.setAttribute("id",y),this.element.setAttribute("aria-describedby",y),this.setContent(),this.config.animation&&a.default(_).addClass(In);var k=typeof this.config.placement=="function"?this.config.placement.call(this,_,this.element):this.config.placement,j=this._getAttachment(k);this.addAttachmentClass(j);var U=this._getContainer();a.default(_).data(this.constructor.DATA_KEY,this),a.default.contains(this.element.ownerDocument.documentElement,this.tip)||a.default(_).appendTo(U),a.default(this.element).trigger(this.constructor.Event.INSERTED),this._popper=new E.default(this.element,_,this._getPopperConfig(j)),a.default(_).addClass(On),a.default(_).addClass(this.config.customClass),"ontouchstart"in document.documentElement&&a.default(document.body).children().on("mouseover",null,a.default.noop);var W=function(){n.config.animation&&n._fixTransition();var ln=n._hoverState;n._hoverState=null,a.default(n.element).trigger(n.constructor.Event.SHOWN),ln===Kt&&n._leave(null,n)};if(a.default(this.tip).hasClass(In)){var ve=D.getTransitionDurationFromElement(this.tip);a.default(this.tip).one(D.TRANSITION_END,W).emulateTransitionEnd(ve)}else W()}},c.hide=function(n){var r=this,l=this.getTipElement(),g=a.default.Event(this.constructor.Event.HIDE),_=function(){r._hoverState!==Nn&&l.parentNode&&l.parentNode.removeChild(l),r._cleanTipClass(),r.element.removeAttribute("aria-describedby"),a.default(r.element).trigger(r.constructor.Event.HIDDEN),r._popper!==null&&r._popper.destroy(),n&&n()};if(a.default(this.element).trigger(g),!g.isDefaultPrevented()){if(a.default(l).removeClass(On),"ontouchstart"in document.documentElement&&a.default(document.body).children().off("mouseover",null,a.default.noop),this._activeTrigger[Tr]=!1,this._activeTrigger[zt]=!1,this._activeTrigger[Mn]=!1,a.default(this.tip).hasClass(In)){var y=D.getTransitionDurationFromElement(l);a.default(l).one(D.TRANSITION_END,_).emulateTransitionEnd(y)}else _();this._hoverState=""}},c.update=function(){this._popper!==null&&this._popper.scheduleUpdate()},c.isWithContent=function(){return!!this.getTitle()},c.addAttachmentClass=function(n){a.default(this.getTipElement()).addClass(Ma+"-"+n)},c.getTipElement=function(){return this.tip=this.tip||a.default(this.config.template)[0],this.tip},c.setContent=function(){var n=this.getTipElement();this.setElementContent(a.default(n.querySelectorAll(Sr)),this.getTitle()),a.default(n).removeClass(In+" "+On)},c.setElementContent=function(n,r){if(typeof r=="object"&&(r.nodeType||r.jquery)){this.config.html?a.default(r).parent().is(n)||n.empty().append(r):n.text(a.default(r).text());return}this.config.html?(this.config.sanitize&&(r=Na(r,this.config.whiteList,this.config.sanitizeFn)),n.html(r)):n.text(r)},c.getTitle=function(){var n=this.element.getAttribute("data-original-title");return n||(n=typeof this.config.title=="function"?this.config.title.call(this.element):this.config.title),n},c._getPopperConfig=function(n){var r=this,l={placement:n,modifiers:{offset:this._getOffset(),flip:{behavior:this.config.fallbackPlacement},arrow:{element:Ar},preventOverflow:{boundariesElement:this.config.boundary}},onCreate:function(_){_.originalPlacement!==_.placement&&r._handlePopperPlacementChange(_)},onUpdate:function(_){return r._handlePopperPlacementChange(_)}};return b({},l,this.config.popperConfig)},c._getOffset=function(){var n=this,r={};return typeof this.config.offset=="function"?r.fn=function(l){return l.offsets=b({},l.offsets,n.config.offset(l.offsets,n.element)),l}:r.offset=this.config.offset,r},c._getContainer=function(){return this.config.container===!1?document.body:D.isElement(this.config.container)?a.default(this.config.container):a.default(document).find(this.config.container)},c._getAttachment=function(n){return Ir[n.toUpperCase()]},c._setListeners=function(){var n=this,r=this.config.trigger.split(" ");r.forEach(function(l){if(l==="click")a.default(n.element).on(n.constructor.Event.CLICK,n.config.selector,function(y){return n.toggle(y)});else if(l!==$r){var g=l===Mn?n.constructor.Event.MOUSEENTER:n.constructor.Event.FOCUSIN,_=l===Mn?n.constructor.Event.MOUSELEAVE:n.constructor.Event.FOCUSOUT;a.default(n.element).on(g,n.config.selector,function(y){return n._enter(y)}).on(_,n.config.selector,function(y){return n._leave(y)})}}),this._hideModalHandler=function(){n.element&&n.hide()},a.default(this.element).closest(".modal").on("hide.bs.modal",this._hideModalHandler),this.config.selector?this.config=b({},this.config,{trigger:"manual",selector:""}):this._fixTitle()},c._fixTitle=function(){var n=typeof this.element.getAttribute("data-original-title");(this.element.getAttribute("title")||n!=="string")&&(this.element.setAttribute("data-original-title",this.element.getAttribute("title")||""),this.element.setAttribute("title",""))},c._enter=function(n,r){var l=this.constructor.DATA_KEY;if(r=r||a.default(n.currentTarget).data(l),r||(r=new this.constructor(n.currentTarget,this._getDelegateConfig()),a.default(n.currentTarget).data(l,r)),n&&(r._activeTrigger[n.type==="focusin"?zt:Mn]=!0),a.default(r.getTipElement()).hasClass(On)||r._hoverState===Nn){r._hoverState=Nn;return}if(clearTimeout(r._timeout),r._hoverState=Nn,!r.config.delay||!r.config.delay.show){r.show();return}r._timeout=setTimeout(function(){r._hoverState===Nn&&r.show()},r.config.delay.show)},c._leave=function(n,r){var l=this.constructor.DATA_KEY;if(r=r||a.default(n.currentTarget).data(l),r||(r=new this.constructor(n.currentTarget,this._getDelegateConfig()),a.default(n.currentTarget).data(l,r)),n&&(r._activeTrigger[n.type==="focusout"?zt:Mn]=!1),!r._isWithActiveTrigger()){if(clearTimeout(r._timeout),r._hoverState=Kt,!r.config.delay||!r.config.delay.hide){r.hide();return}r._timeout=setTimeout(function(){r._hoverState===Kt&&r.hide()},r.config.delay.hide)}},c._isWithActiveTrigger=function(){for(var n in this._activeTrigger)if(this._activeTrigger[n])return!0;return!1},c._getConfig=function(n){var r=a.default(this.element).data();return Object.keys(r).forEach(function(l){Dr.indexOf(l)!==-1&&delete r[l]}),n=b({},this.constructor.Default,r,typeof n=="object"&&n?n:{}),typeof n.delay=="number"&&(n.delay={show:n.delay,hide:n.delay}),typeof n.title=="number"&&(n.title=n.title.toString()),typeof n.content=="number"&&(n.content=n.content.toString()),D.typeCheckConfig(je,n,this.constructor.DefaultType),n.sanitize&&(n.template=Na(n.template,n.whiteList,n.sanitizeFn)),n},c._getDelegateConfig=function(){var n={};if(this.config)for(var r in this.config)this.constructor.Default[r]!==this.config[r]&&(n[r]=this.config[r]);return n},c._cleanTipClass=function(){var n=a.default(this.getTipElement()),r=n.attr("class").match(wr);r!==null&&r.length&&n.removeClass(r.join(""))},c._handlePopperPlacementChange=function(n){this.tip=n.instance.popper,this._cleanTipClass(),this.addAttachmentClass(this._getAttachment(n.placement))},c._fixTransition=function(){var n=this.getTipElement(),r=this.config.animation;n.getAttribute("x-placement")===null&&(a.default(n).removeClass(In),this.config.animation=!1,this.hide(),this.show(),this.config.animation=r)},p._jQueryInterface=function(n){return this.each(function(){var r=a.default(this),l=r.data(it),g=typeof n=="object"&&n;if(!(!l&&/dispose|hide/.test(n))&&(l||(l=new p(this,g),r.data(it,l)),typeof n=="string")){if(typeof l[n]>"u")throw new TypeError('No method named "'+n+'"');l[n]()}})},S(p,null,[{key:"VERSION",get:function(){return br}},{key:"Default",get:function(){return Or}},{key:"NAME",get:function(){return je}},{key:"DATA_KEY",get:function(){return it}},{key:"Event",get:function(){return Mr}},{key:"EVENT_KEY",get:function(){return he}},{key:"DefaultType",get:function(){return Nr}}]),p})();a.default.fn[je]=Ue._jQueryInterface,a.default.fn[je].Constructor=Ue,a.default.fn[je].noConflict=function(){return a.default.fn[je]=Cr,Ue._jQueryInterface};var on="popover",xr="4.6.2",rt="bs.popover",pe="."+rt,kr=a.default.fn[on],xa="bs-popover",Lr=new RegExp("(^|\\s)"+xa+"\\S+","g"),Fr="fade",Pr="show",Rr=".popover-header",jr=".popover-body",Ur=b({},Ue.Default,{placement:"right",trigger:"click",content:"",template:'<div class="popover" role="tooltip"><div class="arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>'}),Br=b({},Ue.DefaultType,{content:"(string|element|function)"}),Hr={HIDE:"hide"+pe,HIDDEN:"hidden"+pe,SHOW:"show"+pe,SHOWN:"shown"+pe,INSERTED:"inserted"+pe,CLICK:"click"+pe,FOCUSIN:"focusin"+pe,FOCUSOUT:"focusout"+pe,MOUSEENTER:"mouseenter"+pe,MOUSELEAVE:"mouseleave"+pe},ot=(function(p){A(c,p);function c(){return p.apply(this,arguments)||this}var u=c.prototype;return u.isWithContent=function(){return this.getTitle()||this._getContent()},u.addAttachmentClass=function(r){a.default(this.getTipElement()).addClass(xa+"-"+r)},u.getTipElement=function(){return this.tip=this.tip||a.default(this.config.template)[0],this.tip},u.setContent=function(){var r=a.default(this.getTipElement());this.setElementContent(r.find(Rr),this.getTitle());var l=this._getContent();typeof l=="function"&&(l=l.call(this.element)),this.setElementContent(r.find(jr),l),r.removeClass(Fr+" "+Pr)},u._getContent=function(){return this.element.getAttribute("data-content")||this.config.content},u._cleanTipClass=function(){var r=a.default(this.getTipElement()),l=r.attr("class").match(Lr);l!==null&&l.length>0&&r.removeClass(l.join(""))},c._jQueryInterface=function(r){return this.each(function(){var l=a.default(this).data(rt),g=typeof r=="object"?r:null;if(!(!l&&/dispose|hide/.test(r))&&(l||(l=new c(this,g),a.default(this).data(rt,l)),typeof r=="string")){if(typeof l[r]>"u")throw new TypeError('No method named "'+r+'"');l[r]()}})},S(c,null,[{key:"VERSION",get:function(){return xr}},{key:"Default",get:function(){return Ur}},{key:"NAME",get:function(){return on}},{key:"DATA_KEY",get:function(){return rt}},{key:"Event",get:function(){return Hr}},{key:"EVENT_KEY",get:function(){return pe}},{key:"DefaultType",get:function(){return Br}}]),c})(Ue);a.default.fn[on]=ot._jQueryInterface,a.default.fn[on].Constructor=ot,a.default.fn[on].noConflict=function(){return a.default.fn[on]=kr,ot._jQueryInterface};var Be="scrollspy",Yr="4.6.2",st="bs.scrollspy",lt="."+st,qr=".data-api",Vr=a.default.fn[Be],Wr="dropdown-item",He="active",Kr="activate"+lt,zr="scroll"+lt,Gr="load"+lt+qr,Qr="offset",ka="position",Jr='[data-spy="scroll"]',La=".nav, .list-group",Gt=".nav-link",Xr=".nav-item",Fa=".list-group-item",Zr=".dropdown",eo=".dropdown-item",no=".dropdown-toggle",Pa={offset:10,method:"auto",target:""},to={offset:"number",method:"string",target:"(string|element)"},xn=(function(){function p(u,n){var r=this;this._element=u,this._scrollElement=u.tagName==="BODY"?window:u,this._config=this._getConfig(n),this._selector=this._config.target+" "+Gt+","+(this._config.target+" "+Fa+",")+(this._config.target+" "+eo),this._offsets=[],this._targets=[],this._activeTarget=null,this._scrollHeight=0,a.default(this._scrollElement).on(zr,function(l){return r._process(l)}),this.refresh(),this._process()}var c=p.prototype;return c.refresh=function(){var n=this,r=this._scrollElement===this._scrollElement.window?Qr:ka,l=this._config.method==="auto"?r:this._config.method,g=l===ka?this._getScrollTop():0;this._offsets=[],this._targets=[],this._scrollHeight=this._getScrollHeight();var _=[].slice.call(document.querySelectorAll(this._selector));_.map(function(y){var k,j=D.getSelectorFromElement(y);if(j&&(k=document.querySelector(j)),k){var U=k.getBoundingClientRect();if(U.width||U.height)return[a.default(k)[l]().top+g,j]}return null}).filter(Boolean).sort(function(y,k){return y[0]-k[0]}).forEach(function(y){n._offsets.push(y[0]),n._targets.push(y[1])})},c.dispose=function(){a.default.removeData(this._element,st),a.default(this._scrollElement).off(lt),this._element=null,this._scrollElement=null,this._config=null,this._selector=null,this._offsets=null,this._targets=null,this._activeTarget=null,this._scrollHeight=null},c._getConfig=function(n){if(n=b({},Pa,typeof n=="object"&&n?n:{}),typeof n.target!="string"&&D.isElement(n.target)){var r=a.default(n.target).attr("id");r||(r=D.getUID(Be),a.default(n.target).attr("id",r)),n.target="#"+r}return D.typeCheckConfig(Be,n,to),n},c._getScrollTop=function(){return this._scrollElement===window?this._scrollElement.pageYOffset:this._scrollElement.scrollTop},c._getScrollHeight=function(){return this._scrollElement.scrollHeight||Math.max(document.body.scrollHeight,document.documentElement.scrollHeight)},c._getOffsetHeight=function(){return this._scrollElement===window?window.innerHeight:this._scrollElement.getBoundingClientRect().height},c._process=function(){var n=this._getScrollTop()+this._config.offset,r=this._getScrollHeight(),l=this._config.offset+r-this._getOffsetHeight();if(this._scrollHeight!==r&&this.refresh(),n>=l){var g=this._targets[this._targets.length-1];this._activeTarget!==g&&this._activate(g);return}if(this._activeTarget&&n<this._offsets[0]&&this._offsets[0]>0){this._activeTarget=null,this._clear();return}for(var _=this._offsets.length;_--;){var y=this._activeTarget!==this._targets[_]&&n>=this._offsets[_]&&(typeof this._offsets[_+1]>"u"||n<this._offsets[_+1]);y&&this._activate(this._targets[_])}},c._activate=function(n){this._activeTarget=n,this._clear();var r=this._selector.split(",").map(function(g){return g+'[data-target="'+n+'"],'+g+'[href="'+n+'"]'}),l=a.default([].slice.call(document.querySelectorAll(r.join(","))));l.hasClass(Wr)?(l.closest(Zr).find(no).addClass(He),l.addClass(He)):(l.addClass(He),l.parents(La).prev(Gt+", "+Fa).addClass(He),l.parents(La).prev(Xr).children(Gt).addClass(He)),a.default(this._scrollElement).trigger(Kr,{relatedTarget:n})},c._clear=function(){[].slice.call(document.querySelectorAll(this._selector)).filter(function(n){return n.classList.contains(He)}).forEach(function(n){return n.classList.remove(He)})},p._jQueryInterface=function(n){return this.each(function(){var r=a.default(this).data(st),l=typeof n=="object"&&n;if(r||(r=new p(this,l),a.default(this).data(st,r)),typeof n=="string"){if(typeof r[n]>"u")throw new TypeError('No method named "'+n+'"');r[n]()}})},S(p,null,[{key:"VERSION",get:function(){return Yr}},{key:"Default",get:function(){return Pa}}]),p})();a.default(window).on(Gr,function(){for(var p=[].slice.call(document.querySelectorAll(Jr)),c=p.length,u=c;u--;){var n=a.default(p[u]);xn._jQueryInterface.call(n,n.data())}}),a.default.fn[Be]=xn._jQueryInterface,a.default.fn[Be].Constructor=xn,a.default.fn[Be].noConflict=function(){return a.default.fn[Be]=Vr,xn._jQueryInterface};var kn="tab",ao="4.6.2",ut="bs.tab",Ln="."+ut,io=".data-api",ro=a.default.fn[kn],oo="dropdown-menu",Fn="active",so="disabled",Ra="fade",ja="show",lo="hide"+Ln,uo="hidden"+Ln,co="show"+Ln,fo="shown"+Ln,ho="click"+Ln+io,po=".dropdown",mo=".nav, .list-group",Ua=".active",Ba="> li > .active",go='[data-toggle="tab"], [data-toggle="pill"], [data-toggle="list"]',vo=".dropdown-toggle",_o="> .dropdown-menu .active",Pn=(function(){function p(u){this._element=u}var c=p.prototype;return c.show=function(){var n=this;if(!(this._element.parentNode&&this._element.parentNode.nodeType===Node.ELEMENT_NODE&&a.default(this._element).hasClass(Fn)||a.default(this._element).hasClass(so)||this._element.hasAttribute("disabled"))){var r,l,g=a.default(this._element).closest(mo)[0],_=D.getSelectorFromElement(this._element);if(g){var y=g.nodeName==="UL"||g.nodeName==="OL"?Ba:Ua;l=a.default.makeArray(a.default(g).find(y)),l=l[l.length-1]}var k=a.default.Event(lo,{relatedTarget:this._element}),j=a.default.Event(co,{relatedTarget:l});if(l&&a.default(l).trigger(k),a.default(this._element).trigger(j),!(j.isDefaultPrevented()||k.isDefaultPrevented())){_&&(r=document.querySelector(_)),this._activate(this._element,g);var U=function(){var ve=a.default.Event(uo,{relatedTarget:n._element}),me=a.default.Event(fo,{relatedTarget:l});a.default(l).trigger(ve),a.default(n._element).trigger(me)};r?this._activate(r,r.parentNode,U):U()}}},c.dispose=function(){a.default.removeData(this._element,ut),this._element=null},c._activate=function(n,r,l){var g=this,_=r&&(r.nodeName==="UL"||r.nodeName==="OL")?a.default(r).find(Ba):a.default(r).children(Ua),y=_[0],k=l&&y&&a.default(y).hasClass(Ra),j=function(){return g._transitionComplete(n,y,l)};if(y&&k){var U=D.getTransitionDurationFromElement(y);a.default(y).removeClass(ja).one(D.TRANSITION_END,j).emulateTransitionEnd(U)}else j()},c._transitionComplete=function(n,r,l){if(r){a.default(r).removeClass(Fn);var g=a.default(r.parentNode).find(_o)[0];g&&a.default(g).removeClass(Fn),r.getAttribute("role")==="tab"&&r.setAttribute("aria-selected",!1)}a.default(n).addClass(Fn),n.getAttribute("role")==="tab"&&n.setAttribute("aria-selected",!0),D.reflow(n),n.classList.contains(Ra)&&n.classList.add(ja);var _=n.parentNode;if(_&&_.nodeName==="LI"&&(_=_.parentNode),_&&a.default(_).hasClass(oo)){var y=a.default(n).closest(po)[0];if(y){var k=[].slice.call(y.querySelectorAll(vo));a.default(k).addClass(Fn)}n.setAttribute("aria-expanded",!0)}l&&l()},p._jQueryInterface=function(n){return this.each(function(){var r=a.default(this),l=r.data(ut);if(l||(l=new p(this),r.data(ut,l)),typeof n=="string"){if(typeof l[n]>"u")throw new TypeError('No method named "'+n+'"');l[n]()}})},S(p,null,[{key:"VERSION",get:function(){return ao}}]),p})();a.default(document).on(ho,go,function(p){p.preventDefault(),Pn._jQueryInterface.call(a.default(this),"show")}),a.default.fn[kn]=Pn._jQueryInterface,a.default.fn[kn].Constructor=Pn,a.default.fn[kn].noConflict=function(){return a.default.fn[kn]=ro,Pn._jQueryInterface};var sn="toast",Eo="4.6.2",ct="bs.toast",Rn="."+ct,yo=a.default.fn[sn],bo="fade",Ha="hide",jn="show",Ya="showing",qa="click.dismiss"+Rn,Co="hide"+Rn,wo="hidden"+Rn,Do="show"+Rn,So="shown"+Rn,Ao='[data-dismiss="toast"]',Va={animation:!0,autohide:!0,delay:500},To={animation:"boolean",autohide:"boolean",delay:"number"},dt=(function(){function p(u,n){this._element=u,this._config=this._getConfig(n),this._timeout=null,this._setListeners()}var c=p.prototype;return c.show=function(){var n=this,r=a.default.Event(Do);if(a.default(this._element).trigger(r),!r.isDefaultPrevented()){this._clearTimeout(),this._config.animation&&this._element.classList.add(bo);var l=function(){n._element.classList.remove(Ya),n._element.classList.add(jn),a.default(n._element).trigger(So),n._config.autohide&&(n._timeout=setTimeout(function(){n.hide()},n._config.delay))};if(this._element.classList.remove(Ha),D.reflow(this._element),this._element.classList.add(Ya),this._config.animation){var g=D.getTransitionDurationFromElement(this._element);a.default(this._element).one(D.TRANSITION_END,l).emulateTransitionEnd(g)}else l()}},c.hide=function(){if(this._element.classList.contains(jn)){var n=a.default.Event(Co);a.default(this._element).trigger(n),!n.isDefaultPrevented()&&this._close()}},c.dispose=function(){this._clearTimeout(),this._element.classList.contains(jn)&&this._element.classList.remove(jn),a.default(this._element).off(qa),a.default.removeData(this._element,ct),this._element=null,this._config=null},c._getConfig=function(n){return n=b({},Va,a.default(this._element).data(),typeof n=="object"&&n?n:{}),D.typeCheckConfig(sn,n,this.constructor.DefaultType),n},c._setListeners=function(){var n=this;a.default(this._element).on(qa,Ao,function(){return n.hide()})},c._close=function(){var n=this,r=function(){n._element.classList.add(Ha),a.default(n._element).trigger(wo)};if(this._element.classList.remove(jn),this._config.animation){var l=D.getTransitionDurationFromElement(this._element);a.default(this._element).one(D.TRANSITION_END,r).emulateTransitionEnd(l)}else r()},c._clearTimeout=function(){clearTimeout(this._timeout),this._timeout=null},p._jQueryInterface=function(n){return this.each(function(){var r=a.default(this),l=r.data(ct),g=typeof n=="object"&&n;if(l||(l=new p(this,g),r.data(ct,l)),typeof n=="string"){if(typeof l[n]>"u")throw new TypeError('No method named "'+n+'"');l[n](this)}})},S(p,null,[{key:"VERSION",get:function(){return Eo}},{key:"DefaultType",get:function(){return To}},{key:"Default",get:function(){return Va}}]),p})();a.default.fn[sn]=dt._jQueryInterface,a.default.fn[sn].Constructor=dt,a.default.fn[sn].noConflict=function(){return a.default.fn[sn]=yo,dt._jQueryInterface},e.Alert=Ee,e.Button=Te,e.Carousel=Oe,e.Collapse=Dn,e.Dropdown=Me,e.Modal=$n,e.Popover=ot,e.Scrollspy=xn,e.Tab=Pn,e.Toast=dt,e.Tooltip=Ue,e.Util=D,Object.defineProperty(e,"__esModule",{value:!0})}))})(Un,Un.exports)),Un.exports}Es();var Zt=["onChange","onClose","onDayCreate","onDestroy","onKeyDown","onMonthChange","onOpen","onParseConfig","onReady","onValueUpdate","onYearChange","onPreCalendarPosition"],un={_disable:[],allowInput:!1,allowInvalidPreload:!1,altFormat:"F j, Y",altInput:!1,altInputClass:"form-control input",animate:typeof window=="object"&&window.navigator.userAgent.indexOf("MSIE")===-1,ariaDateFormat:"F j, Y",autoFillDefaultTime:!0,clickOpens:!0,closeOnSelect:!0,conjunction:", ",dateFormat:"Y-m-d",defaultHour:12,defaultMinute:0,defaultSeconds:0,disable:[],disableMobile:!1,enableSeconds:!1,enableTime:!1,errorHandler:function(t){return typeof console<"u"&&console.warn(t)},getWeek:function(t){var i=new Date(t.getTime());i.setHours(0,0,0,0),i.setDate(i.getDate()+3-(i.getDay()+6)%7);var e=new Date(i.getFullYear(),0,4);return 1+Math.round(((i.getTime()-e.getTime())/864e5-3+(e.getDay()+6)%7)/7)},hourIncrement:1,ignoredFocusElements:[],inline:!1,locale:"default",minuteIncrement:5,mode:"single",monthSelectorType:"dropdown",nextArrow:"<svg version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' viewBox='0 0 17 17'><g></g><path d='M13.207 8.472l-7.854 7.854-0.707-0.707 7.146-7.146-7.146-7.148 0.707-0.707 7.854 7.854z' /></svg>",noCalendar:!1,now:new Date,onChange:[],onClose:[],onDayCreate:[],onDestroy:[],onKeyDown:[],onMonthChange:[],onOpen:[],onParseConfig:[],onReady:[],onValueUpdate:[],onYearChange:[],onPreCalendarPosition:[],plugins:[],position:"auto",positionElement:void 0,prevArrow:"<svg version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' viewBox='0 0 17 17'><g></g><path d='M5.207 8.471l7.146 7.147-0.707 0.707-7.853-7.854 7.854-7.853 0.707 0.707-7.147 7.146z' /></svg>",shorthandCurrentMonth:!1,showMonths:1,static:!1,time_24hr:!1,weekNumbers:!1,wrap:!1},Hn={weekdays:{shorthand:["Sun","Mon","Tue","Wed","Thu","Fri","Sat"],longhand:["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]},months:{shorthand:["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],longhand:["January","February","March","April","May","June","July","August","September","October","November","December"]},daysInMonth:[31,28,31,30,31,30,31,31,30,31,30,31],firstDayOfWeek:0,ordinal:function(t){var i=t%100;if(i>3&&i<21)return"th";switch(i%10){case 1:return"st";case 2:return"nd";case 3:return"rd";default:return"th"}},rangeSeparator:" to ",weekAbbreviation:"Wk",scrollTitle:"Scroll to increment",toggleTitle:"Click to toggle",amPM:["AM","PM"],yearAriaLabel:"Year",monthAriaLabel:"Month",hourAriaLabel:"Hour",minuteAriaLabel:"Minute",time_24hr:!1},ne=function(t,i){return i===void 0&&(i=2),("000"+t).slice(i*-1)},se=function(t){return t===!0?1:0};function ei(t,i){var e;return function(){var d=this,m=arguments;clearTimeout(e),e=setTimeout(function(){return t.apply(d,m)},i)}}var ea=function(t){return t instanceof Array?t:[t]};function Z(t,i,e){if(e===!0)return t.classList.add(i);t.classList.remove(i)}function B(t,i,e){var d=window.document.createElement(t);return i=i||"",e=e||"",d.className=i,e!==void 0&&(d.textContent=e),d}function ft(t){for(;t.firstChild;)t.removeChild(t.firstChild)}function _i(t,i){if(i(t))return t;if(t.parentNode)return _i(t.parentNode,i)}function ht(t,i){var e=B("div","numInputWrapper"),d=B("input","numInput "+t),m=B("span","arrowUp"),h=B("span","arrowDown");if(navigator.userAgent.indexOf("MSIE 9.0")===-1?d.type="number":(d.type="text",d.pattern="\\d*"),i!==void 0)for(var a in i)d.setAttribute(a,i[a]);return e.appendChild(d),e.appendChild(m),e.appendChild(h),e}function ae(t){try{if(typeof t.composedPath=="function"){var i=t.composedPath();return i[0]}return t.target}catch{return t.target}}var na=function(){},gt=function(t,i,e){return e.months[i?"shorthand":"longhand"][t]},ys={D:na,F:function(t,i,e){t.setMonth(e.months.longhand.indexOf(i))},G:function(t,i){t.setHours((t.getHours()>=12?12:0)+parseFloat(i))},H:function(t,i){t.setHours(parseFloat(i))},J:function(t,i){t.setDate(parseFloat(i))},K:function(t,i,e){t.setHours(t.getHours()%12+12*se(new RegExp(e.amPM[1],"i").test(i)))},M:function(t,i,e){t.setMonth(e.months.shorthand.indexOf(i))},S:function(t,i){t.setSeconds(parseFloat(i))},U:function(t,i){return new Date(parseFloat(i)*1e3)},W:function(t,i,e){var d=parseInt(i),m=new Date(t.getFullYear(),0,2+(d-1)*7,0,0,0,0);return m.setDate(m.getDate()-m.getDay()+e.firstDayOfWeek),m},Y:function(t,i){t.setFullYear(parseFloat(i))},Z:function(t,i){return new Date(i)},d:function(t,i){t.setDate(parseFloat(i))},h:function(t,i){t.setHours((t.getHours()>=12?12:0)+parseFloat(i))},i:function(t,i){t.setMinutes(parseFloat(i))},j:function(t,i){t.setDate(parseFloat(i))},l:na,m:function(t,i){t.setMonth(parseFloat(i)-1)},n:function(t,i){t.setMonth(parseFloat(i)-1)},s:function(t,i){t.setSeconds(parseFloat(i))},u:function(t,i){return new Date(parseFloat(i))},w:na,y:function(t,i){t.setFullYear(2e3+parseFloat(i))}},Ye={D:"",F:"",G:"(\\d\\d|\\d)",H:"(\\d\\d|\\d)",J:"(\\d\\d|\\d)\\w+",K:"",M:"",S:"(\\d\\d|\\d)",U:"(.+)",W:"(\\d\\d|\\d)",Y:"(\\d{4})",Z:"(.+)",d:"(\\d\\d|\\d)",h:"(\\d\\d|\\d)",i:"(\\d\\d|\\d)",j:"(\\d\\d|\\d)",l:"",m:"(\\d\\d|\\d)",n:"(\\d\\d|\\d)",s:"(\\d\\d|\\d)",u:"(.+)",w:"(\\d\\d|\\d)",y:"(\\d{2})"},Bn={Z:function(t){return t.toISOString()},D:function(t,i,e){return i.weekdays.shorthand[Bn.w(t,i,e)]},F:function(t,i,e){return gt(Bn.n(t,i,e)-1,!1,i)},G:function(t,i,e){return ne(Bn.h(t,i,e))},H:function(t){return ne(t.getHours())},J:function(t,i){return i.ordinal!==void 0?t.getDate()+i.ordinal(t.getDate()):t.getDate()},K:function(t,i){return i.amPM[se(t.getHours()>11)]},M:function(t,i){return gt(t.getMonth(),!0,i)},S:function(t){return ne(t.getSeconds())},U:function(t){return t.getTime()/1e3},W:function(t,i,e){return e.getWeek(t)},Y:function(t){return ne(t.getFullYear(),4)},d:function(t){return ne(t.getDate())},h:function(t){return t.getHours()%12?t.getHours()%12:12},i:function(t){return ne(t.getMinutes())},j:function(t){return t.getDate()},l:function(t,i){return i.weekdays.longhand[t.getDay()]},m:function(t){return ne(t.getMonth()+1)},n:function(t){return t.getMonth()+1},s:function(t){return t.getSeconds()},u:function(t){return t.getTime()},w:function(t){return t.getDay()},y:function(t){return String(t.getFullYear()).substring(2)}},Ei=function(t){var i=t.config,e=i===void 0?un:i,d=t.l10n,m=d===void 0?Hn:d,h=t.isMobile,a=h===void 0?!1:h;return function(E,C,S){var b=S||m;return e.formatDate!==void 0&&!a?e.formatDate(E,C,b):C.split("").map(function(A,N,O){return Bn[A]&&O[N-1]!=="\\"?Bn[A](E,b,e):A!=="\\"?A:""}).join("")}},sa=function(t){var i=t.config,e=i===void 0?un:i,d=t.l10n,m=d===void 0?Hn:d;return function(h,a,E,C){if(!(h!==0&&!h)){var S=C||m,b,A=h;if(h instanceof Date)b=new Date(h.getTime());else if(typeof h!="string"&&h.toFixed!==void 0)b=new Date(h);else if(typeof h=="string"){var N=a||(e||un).dateFormat,O=String(h).trim();if(O==="today")b=new Date,E=!0;else if(e&&e.parseDate)b=e.parseDate(h,N);else if(/Z$/.test(O)||/GMT$/.test(O))b=new Date(h);else{for(var L=void 0,M=[],V=0,ee=0,Y="";V<N.length;V++){var K=N[V],D=K==="\\",re=N[V-1]==="\\"||D;if(Ye[K]&&!re){Y+=Ye[K];var _e=new RegExp(Y).exec(h);_e&&(L=!0)&&M[K!=="Y"?"push":"unshift"]({fn:ys[K],val:_e[++ee]})}else D||(Y+=".")}b=!e||!e.noCalendar?new Date(new Date().getFullYear(),0,1,0,0,0,0):new Date(new Date().setHours(0,0,0,0)),M.forEach(function(ue){var ge=ue.fn,mn=ue.val;return b=ge(b,mn,S)||b}),b=L?b:void 0}}if(!(b instanceof Date&&!isNaN(b.getTime()))){e.errorHandler(new Error("Invalid date provided: "+A));return}return E===!0&&b.setHours(0,0,0,0),b}}};function ie(t,i,e){return e===void 0&&(e=!0),e!==!1?new Date(t.getTime()).setHours(0,0,0,0)-new Date(i.getTime()).setHours(0,0,0,0):t.getTime()-i.getTime()}var bs=function(t,i,e){return t>Math.min(i,e)&&t<Math.max(i,e)},ta=function(t,i,e){return t*3600+i*60+e},Cs=function(t){var i=Math.floor(t/3600),e=(t-i*3600)/60;return[i,e,t-i*3600-e*60]},ws={DAY:864e5};function aa(t){var i=t.defaultHour,e=t.defaultMinute,d=t.defaultSeconds;if(t.minDate!==void 0){var m=t.minDate.getHours(),h=t.minDate.getMinutes(),a=t.minDate.getSeconds();i<m&&(i=m),i===m&&e<h&&(e=h),i===m&&e===h&&d<a&&(d=t.minDate.getSeconds())}if(t.maxDate!==void 0){var E=t.maxDate.getHours(),C=t.maxDate.getMinutes();i=Math.min(i,E),i===E&&(e=Math.min(C,e)),i===E&&e===C&&(d=t.maxDate.getSeconds())}return{hours:i,minutes:e,seconds:d}}typeof Object.assign!="function"&&(Object.assign=function(t){for(var i=[],e=1;e<arguments.length;e++)i[e-1]=arguments[e];if(!t)throw TypeError("Cannot convert undefined or null to object");for(var d=function(E){E&&Object.keys(E).forEach(function(C){return t[C]=E[C]})},m=0,h=i;m<h.length;m++){var a=h[m];d(a)}return t});var Q=function(){return Q=Object.assign||function(t){for(var i,e=1,d=arguments.length;e<d;e++){i=arguments[e];for(var m in i)Object.prototype.hasOwnProperty.call(i,m)&&(t[m]=i[m])}return t},Q.apply(this,arguments)},ni=function(){for(var t=0,i=0,e=arguments.length;i<e;i++)t+=arguments[i].length;for(var d=Array(t),m=0,i=0;i<e;i++)for(var h=arguments[i],a=0,E=h.length;a<E;a++,m++)d[m]=h[a];return d},Ds=300;function Ss(t,i){var e={config:Q(Q({},un),q.defaultConfig),l10n:Hn};e.parseDate=sa({config:e.config,l10n:e.l10n}),e._handlers=[],e.pluginElements=[],e.loadedPlugins=[],e._bind=M,e._setHoursFromDate=N,e._positionCalendar=ce,e.changeMonth=Ae,e.changeYear=ze,e.clear=We,e.close=Ke,e.onMouseOver=Qe,e._createElement=B,e.createDay=_e,e.destroy=wt,e.isEnabled=ye,e.jumpToDate=Y,e.updateValue=de,e.open=At,e.redraw=z,e.set=It,e.setDate=Ot,e.toggle=xt;function d(){e.utils={getDaysInMonth:function(o,s){return o===void 0&&(o=e.currentMonth),s===void 0&&(s=e.currentYear),o===1&&(s%4===0&&s%100!==0||s%400===0)?29:e.l10n.daysInMonth[o]}}}function m(){e.element=e.input=t,e.isOpen=!1,Tt(),Te(),Nt(),be(),d(),e.isMobile||re(),ee(),(e.selectedDates.length||e.config.noCalendar)&&(e.config.enableTime&&N(e.config.noCalendar?e.latestSelectedDateObj:void 0),de(!1)),E();var o=/^((?!chrome|android).)*safari/i.test(navigator.userAgent);!e.isMobile&&o&&ce(),H("onReady")}function h(){var o;return((o=e.calendarContainer)===null||o===void 0?void 0:o.getRootNode()).activeElement||document.activeElement}function a(o){return o.bind(e)}function E(){var o=e.config;o.weekNumbers===!1&&o.showMonths===1||o.noCalendar!==!0&&window.requestAnimationFrame(function(){if(e.calendarContainer!==void 0&&(e.calendarContainer.style.visibility="hidden",e.calendarContainer.style.display="block"),e.daysContainer!==void 0){var s=(e.days.offsetWidth+1)*o.showMonths;e.daysContainer.style.width=s+"px",e.calendarContainer.style.width=s+(e.weekWrapper!==void 0?e.weekWrapper.offsetWidth:0)+"px",e.calendarContainer.style.removeProperty("visibility"),e.calendarContainer.style.removeProperty("display")}})}function C(o){if(e.selectedDates.length===0){var s=e.config.minDate===void 0||ie(new Date,e.config.minDate)>=0?new Date:new Date(e.config.minDate.getTime()),f=aa(e.config);s.setHours(f.hours,f.minutes,f.seconds,s.getMilliseconds()),e.selectedDates=[s],e.latestSelectedDateObj=s}o!==void 0&&o.type!=="blur"&&kt(o);var v=e._input.value;A(),de(),e._input.value!==v&&e._debouncedChange()}function S(o,s){return o%12+12*se(s===e.l10n.amPM[1])}function b(o){switch(o%24){case 0:case 12:return 12;default:return o%12}}function A(){if(!(e.hourElement===void 0||e.minuteElement===void 0)){var o=(parseInt(e.hourElement.value.slice(-2),10)||0)%24,s=(parseInt(e.minuteElement.value,10)||0)%60,f=e.secondElement!==void 0?(parseInt(e.secondElement.value,10)||0)%60:0;e.amPM!==void 0&&(o=S(o,e.amPM.textContent));var v=e.config.minTime!==void 0||e.config.minDate&&e.minDateHasTime&&e.latestSelectedDateObj&&ie(e.latestSelectedDateObj,e.config.minDate,!0)===0,w=e.config.maxTime!==void 0||e.config.maxDate&&e.maxDateHasTime&&e.latestSelectedDateObj&&ie(e.latestSelectedDateObj,e.config.maxDate,!0)===0;if(e.config.maxTime!==void 0&&e.config.minTime!==void 0&&e.config.minTime>e.config.maxTime){var T=ta(e.config.minTime.getHours(),e.config.minTime.getMinutes(),e.config.minTime.getSeconds()),F=ta(e.config.maxTime.getHours(),e.config.maxTime.getMinutes(),e.config.maxTime.getSeconds()),I=ta(o,s,f);if(I>F&&I<T){var P=Cs(T);o=P[0],s=P[1],f=P[2]}}else{if(w){var $=e.config.maxTime!==void 0?e.config.maxTime:e.config.maxDate;o=Math.min(o,$.getHours()),o===$.getHours()&&(s=Math.min(s,$.getMinutes())),s===$.getMinutes()&&(f=Math.min(f,$.getSeconds()))}if(v){var x=e.config.minTime!==void 0?e.config.minTime:e.config.minDate;o=Math.max(o,x.getHours()),o===x.getHours()&&s<x.getMinutes()&&(s=x.getMinutes()),s===x.getMinutes()&&(f=Math.max(f,x.getSeconds()))}}O(o,s,f)}}function N(o){var s=o||e.latestSelectedDateObj;s&&s instanceof Date&&O(s.getHours(),s.getMinutes(),s.getSeconds())}function O(o,s,f){e.latestSelectedDateObj!==void 0&&e.latestSelectedDateObj.setHours(o%24,s,f||0,0),!(!e.hourElement||!e.minuteElement||e.isMobile)&&(e.hourElement.value=ne(e.config.time_24hr?o:(12+o)%12+12*se(o%12===0)),e.minuteElement.value=ne(s),e.amPM!==void 0&&(e.amPM.textContent=e.l10n.amPM[se(o>=12)]),e.secondElement!==void 0&&(e.secondElement.value=ne(f)))}function L(o){var s=ae(o),f=parseInt(s.value)+(o.delta||0);(f/1e3>1||o.key==="Enter"&&!/[^\d]/.test(f.toString()))&&ze(f)}function M(o,s,f,v){if(s instanceof Array)return s.forEach(function(w){return M(o,w,f,v)});if(o instanceof Array)return o.forEach(function(w){return M(w,s,f,v)});o.addEventListener(s,f,v),e._handlers.push({remove:function(){return o.removeEventListener(s,f,v)}})}function V(){H("onChange")}function ee(){if(e.config.wrap&&["open","close","toggle","clear"].forEach(function(f){Array.prototype.forEach.call(e.element.querySelectorAll("[data-"+f+"]"),function(v){return M(v,"click",e[f])})}),e.isMobile){Mt();return}var o=ei(St,50);if(e._debouncedChange=ei(V,Ds),e.daysContainer&&!/iPhone|iPad|iPod/i.test(navigator.userAgent)&&M(e.daysContainer,"mouseover",function(f){e.config.mode==="range"&&Qe(ae(f))}),M(e._input,"keydown",vn),e.calendarContainer!==void 0&&M(e.calendarContainer,"keydown",vn),!e.config.inline&&!e.config.static&&M(window,"resize",o),window.ontouchstart!==void 0?M(window.document,"touchstart",gn):M(window.document,"mousedown",gn),M(window.document,"focus",gn,{capture:!0}),e.config.clickOpens===!0&&(M(e._input,"focus",e.open),M(e._input,"click",e.open)),e.daysContainer!==void 0&&(M(e.monthNav,"click",Jn),M(e.monthNav,["keyup","increment"],L),M(e.daysContainer,"click",Kn)),e.timeContainer!==void 0&&e.minuteElement!==void 0&&e.hourElement!==void 0){var s=function(f){return ae(f).select()};M(e.timeContainer,["increment"],C),M(e.timeContainer,"blur",C,{capture:!0}),M(e.timeContainer,"click",K),M([e.hourElement,e.minuteElement],["focus","click"],s),e.secondElement!==void 0&&M(e.secondElement,"focus",function(){return e.secondElement&&e.secondElement.select()}),e.amPM!==void 0&&M(e.amPM,"click",function(f){C(f)})}e.config.allowInput&&M(e._input,"blur",Dt)}function Y(o,s){var f=o!==void 0?e.parseDate(o):e.latestSelectedDateObj||(e.config.minDate&&e.config.minDate>e.now?e.config.minDate:e.config.maxDate&&e.config.maxDate<e.now?e.config.maxDate:e.now),v=e.currentYear,w=e.currentMonth;try{f!==void 0&&(e.currentYear=f.getFullYear(),e.currentMonth=f.getMonth())}catch(T){T.message="Invalid date supplied: "+f,e.config.errorHandler(T)}s&&e.currentYear!==v&&(H("onYearChange"),De()),s&&(e.currentYear!==v||e.currentMonth!==w)&&H("onMonthChange"),e.redraw()}function K(o){var s=ae(o);~s.className.indexOf("arrow")&&D(o,s.classList.contains("arrowUp")?1:-1)}function D(o,s,f){var v=o&&ae(o),w=f||v&&v.parentNode&&v.parentNode.firstChild,T=En("increment");T.delta=s,w&&w.dispatchEvent(T)}function re(){var o=window.document.createDocumentFragment();if(e.calendarContainer=B("div","flatpickr-calendar"),e.calendarContainer.tabIndex=-1,!e.config.noCalendar){if(o.appendChild(yt()),e.innerContainer=B("div","flatpickr-innerContainer"),e.config.weekNumbers){var s=Ct(),f=s.weekWrapper,v=s.weekNumbers;e.innerContainer.appendChild(f),e.weekNumbers=v,e.weekWrapper=f}e.rContainer=B("div","flatpickr-rContainer"),e.rContainer.appendChild(Ee()),e.daysContainer||(e.daysContainer=B("div","flatpickr-days"),e.daysContainer.tabIndex=-1),Ve(),e.rContainer.appendChild(e.daysContainer),e.innerContainer.appendChild(e.rContainer),o.appendChild(e.innerContainer)}e.config.enableTime&&o.appendChild(bt()),Z(e.calendarContainer,"rangeMode",e.config.mode==="range"),Z(e.calendarContainer,"animate",e.config.animate===!0),Z(e.calendarContainer,"multiMonth",e.config.showMonths>1),e.calendarContainer.appendChild(o);var w=e.config.appendTo!==void 0&&e.config.appendTo.nodeType!==void 0;if((e.config.inline||e.config.static)&&(e.calendarContainer.classList.add(e.config.inline?"inline":"static"),e.config.inline&&(!w&&e.element.parentNode?e.element.parentNode.insertBefore(e.calendarContainer,e._input.nextSibling):e.config.appendTo!==void 0&&e.config.appendTo.appendChild(e.calendarContainer)),e.config.static)){var T=B("div","flatpickr-wrapper");e.element.parentNode&&e.element.parentNode.insertBefore(T,e.element),T.appendChild(e.element),e.altInput&&T.appendChild(e.altInput),T.appendChild(e.calendarContainer)}!e.config.static&&!e.config.inline&&(e.config.appendTo!==void 0?e.config.appendTo:window.document.body).appendChild(e.calendarContainer)}function _e(o,s,f,v){var w=ye(s,!0),T=B("span",o,s.getDate().toString());return T.dateObj=s,T.$i=v,T.setAttribute("aria-label",e.formatDate(s,e.config.ariaDateFormat)),o.indexOf("hidden")===-1&&ie(s,e.now)===0&&(e.todayDateElem=T,T.classList.add("today"),T.setAttribute("aria-current","date")),w?(T.tabIndex=-1,$e(s)&&(T.classList.add("selected"),e.selectedDateElem=T,e.config.mode==="range"&&(Z(T,"startRange",e.selectedDates[0]&&ie(s,e.selectedDates[0],!0)===0),Z(T,"endRange",e.selectedDates[1]&&ie(s,e.selectedDates[1],!0)===0),o==="nextMonthDay"&&T.classList.add("inRange")))):T.classList.add("flatpickr-disabled"),e.config.mode==="range"&&en(s)&&!$e(s)&&T.classList.add("inRange"),e.weekNumbers&&e.config.showMonths===1&&o!=="prevMonthDay"&&v%7===6&&e.weekNumbers.insertAdjacentHTML("beforeend","<span class='flatpickr-day'>"+e.config.getWeek(s)+"</span>"),H("onDayCreate",T),T}function ue(o){o.focus(),e.config.mode==="range"&&Qe(o)}function ge(o){for(var s=o>0?0:e.config.showMonths-1,f=o>0?e.config.showMonths:-1,v=s;v!=f;v+=o)for(var w=e.daysContainer.children[v],T=o>0?0:w.children.length-1,F=o>0?w.children.length:-1,I=T;I!=F;I+=o){var P=w.children[I];if(P.className.indexOf("hidden")===-1&&ye(P.dateObj))return P}}function mn(o,s){for(var f=o.className.indexOf("Month")===-1?o.dateObj.getMonth():e.currentMonth,v=s>0?e.config.showMonths:-1,w=s>0?1:-1,T=f-e.currentMonth;T!=v;T+=w)for(var F=e.daysContainer.children[T],I=f-e.currentMonth===T?o.$i+s:s<0?F.children.length-1:0,P=F.children.length,$=I;$>=0&&$<P&&$!=(s>0?P:-1);$+=w){var x=F.children[$];if(x.className.indexOf("hidden")===-1&&ye(x.dateObj)&&Math.abs(o.$i-$)>=Math.abs(s))return ue(x)}e.changeMonth(w),ke(ge(w),0)}function ke(o,s){var f=h(),v=Ge(f||document.body),w=o!==void 0?o:v?f:e.selectedDateElem!==void 0&&Ge(e.selectedDateElem)?e.selectedDateElem:e.todayDateElem!==void 0&&Ge(e.todayDateElem)?e.todayDateElem:ge(s>0?1:-1);w===void 0?e._input.focus():v?mn(w,s):ue(w)}function _t(o,s){for(var f=(new Date(o,s,1).getDay()-e.l10n.firstDayOfWeek+7)%7,v=e.utils.getDaysInMonth((s-1+12)%12,o),w=e.utils.getDaysInMonth(s,o),T=window.document.createDocumentFragment(),F=e.config.showMonths>1,I=F?"prevMonthDay hidden":"prevMonthDay",P=F?"nextMonthDay hidden":"nextMonthDay",$=v+1-f,x=0;$<=v;$++,x++)T.appendChild(_e("flatpickr-day "+I,new Date(o,s-1,$),$,x));for($=1;$<=w;$++,x++)T.appendChild(_e("flatpickr-day",new Date(o,s,$),$,x));for(var R=w+1;R<=42-f&&(e.config.showMonths===1||x%7!==0);R++,x++)T.appendChild(_e("flatpickr-day "+P,new Date(o,s+1,R%w),R,x));var oe=B("div","dayContainer");return oe.appendChild(T),oe}function Ve(){if(e.daysContainer!==void 0){ft(e.daysContainer),e.weekNumbers&&ft(e.weekNumbers);for(var o=document.createDocumentFragment(),s=0;s<e.config.showMonths;s++){var f=new Date(e.currentYear,e.currentMonth,1);f.setMonth(e.currentMonth+s),o.appendChild(_t(f.getFullYear(),f.getMonth()))}e.daysContainer.appendChild(o),e.days=e.daysContainer.firstChild,e.config.mode==="range"&&e.selectedDates.length===1&&Qe()}}function De(){if(!(e.config.showMonths>1||e.config.monthSelectorType!=="dropdown")){var o=function(v){return e.config.minDate!==void 0&&e.currentYear===e.config.minDate.getFullYear()&&v<e.config.minDate.getMonth()?!1:!(e.config.maxDate!==void 0&&e.currentYear===e.config.maxDate.getFullYear()&&v>e.config.maxDate.getMonth())};e.monthsDropdownContainer.tabIndex=-1,e.monthsDropdownContainer.innerHTML="";for(var s=0;s<12;s++)if(o(s)){var f=B("option","flatpickr-monthDropdown-month");f.value=new Date(e.currentYear,s).getMonth().toString(),f.textContent=gt(s,e.config.shorthandCurrentMonth,e.l10n),f.tabIndex=-1,e.currentMonth===s&&(f.selected=!0),e.monthsDropdownContainer.appendChild(f)}}}function Et(){var o=B("div","flatpickr-month"),s=window.document.createDocumentFragment(),f;e.config.showMonths>1||e.config.monthSelectorType==="static"?f=B("span","cur-month"):(e.monthsDropdownContainer=B("select","flatpickr-monthDropdown-months"),e.monthsDropdownContainer.setAttribute("aria-label",e.l10n.monthAriaLabel),M(e.monthsDropdownContainer,"change",function(F){var I=ae(F),P=parseInt(I.value,10);e.changeMonth(P-e.currentMonth),H("onMonthChange")}),De(),f=e.monthsDropdownContainer);var v=ht("cur-year",{tabindex:"-1"}),w=v.getElementsByTagName("input")[0];w.setAttribute("aria-label",e.l10n.yearAriaLabel),e.config.minDate&&w.setAttribute("min",e.config.minDate.getFullYear().toString()),e.config.maxDate&&(w.setAttribute("max",e.config.maxDate.getFullYear().toString()),w.disabled=!!e.config.minDate&&e.config.minDate.getFullYear()===e.config.maxDate.getFullYear());var T=B("div","flatpickr-current-month");return T.appendChild(f),T.appendChild(v),s.appendChild(T),o.appendChild(s),{container:o,yearElement:w,monthElement:f}}function Wn(){ft(e.monthNav),e.monthNav.appendChild(e.prevMonthNav),e.config.showMonths&&(e.yearElements=[],e.monthElements=[]);for(var o=e.config.showMonths;o--;){var s=Et();e.yearElements.push(s.yearElement),e.monthElements.push(s.monthElement),e.monthNav.appendChild(s.container)}e.monthNav.appendChild(e.nextMonthNav)}function yt(){return e.monthNav=B("div","flatpickr-months"),e.yearElements=[],e.monthElements=[],e.prevMonthNav=B("span","flatpickr-prev-month"),e.prevMonthNav.innerHTML=e.config.prevArrow,e.nextMonthNav=B("span","flatpickr-next-month"),e.nextMonthNav.innerHTML=e.config.nextArrow,Wn(),Object.defineProperty(e,"_hidePrevMonthArrow",{get:function(){return e.__hidePrevMonthArrow},set:function(o){e.__hidePrevMonthArrow!==o&&(Z(e.prevMonthNav,"flatpickr-disabled",o),e.__hidePrevMonthArrow=o)}}),Object.defineProperty(e,"_hideNextMonthArrow",{get:function(){return e.__hideNextMonthArrow},set:function(o){e.__hideNextMonthArrow!==o&&(Z(e.nextMonthNav,"flatpickr-disabled",o),e.__hideNextMonthArrow=o)}}),e.currentYearElement=e.yearElements[0],nn(),e.monthNav}function bt(){e.calendarContainer.classList.add("hasTime"),e.config.noCalendar&&e.calendarContainer.classList.add("noCalendar");var o=aa(e.config);e.timeContainer=B("div","flatpickr-time"),e.timeContainer.tabIndex=-1;var s=B("span","flatpickr-time-separator",":"),f=ht("flatpickr-hour",{"aria-label":e.l10n.hourAriaLabel});e.hourElement=f.getElementsByTagName("input")[0];var v=ht("flatpickr-minute",{"aria-label":e.l10n.minuteAriaLabel});if(e.minuteElement=v.getElementsByTagName("input")[0],e.hourElement.tabIndex=e.minuteElement.tabIndex=-1,e.hourElement.value=ne(e.latestSelectedDateObj?e.latestSelectedDateObj.getHours():e.config.time_24hr?o.hours:b(o.hours)),e.minuteElement.value=ne(e.latestSelectedDateObj?e.latestSelectedDateObj.getMinutes():o.minutes),e.hourElement.setAttribute("step",e.config.hourIncrement.toString()),e.minuteElement.setAttribute("step",e.config.minuteIncrement.toString()),e.hourElement.setAttribute("min",e.config.time_24hr?"0":"1"),e.hourElement.setAttribute("max",e.config.time_24hr?"23":"12"),e.hourElement.setAttribute("maxlength","2"),e.minuteElement.setAttribute("min","0"),e.minuteElement.setAttribute("max","59"),e.minuteElement.setAttribute("maxlength","2"),e.timeContainer.appendChild(f),e.timeContainer.appendChild(s),e.timeContainer.appendChild(v),e.config.time_24hr&&e.timeContainer.classList.add("time24hr"),e.config.enableSeconds){e.timeContainer.classList.add("hasSeconds");var w=ht("flatpickr-second");e.secondElement=w.getElementsByTagName("input")[0],e.secondElement.value=ne(e.latestSelectedDateObj?e.latestSelectedDateObj.getSeconds():o.seconds),e.secondElement.setAttribute("step",e.minuteElement.getAttribute("step")),e.secondElement.setAttribute("min","0"),e.secondElement.setAttribute("max","59"),e.secondElement.setAttribute("maxlength","2"),e.timeContainer.appendChild(B("span","flatpickr-time-separator",":")),e.timeContainer.appendChild(w)}return e.config.time_24hr||(e.amPM=B("span","flatpickr-am-pm",e.l10n.amPM[se((e.latestSelectedDateObj?e.hourElement.value:e.config.defaultHour)>11)]),e.amPM.title=e.l10n.toggleTitle,e.amPM.tabIndex=-1,e.timeContainer.appendChild(e.amPM)),e.timeContainer}function Ee(){e.weekdayContainer?ft(e.weekdayContainer):e.weekdayContainer=B("div","flatpickr-weekdays");for(var o=e.config.showMonths;o--;){var s=B("div","flatpickr-weekdaycontainer");e.weekdayContainer.appendChild(s)}return Se(),e.weekdayContainer}function Se(){if(e.weekdayContainer){var o=e.l10n.firstDayOfWeek,s=ni(e.l10n.weekdays.shorthand);o>0&&o<s.length&&(s=ni(s.splice(o,s.length),s.splice(0,o)));for(var f=e.config.showMonths;f--;)e.weekdayContainer.children[f].innerHTML=`
      <span class='flatpickr-weekday'>
        `+s.join("</span><span class='flatpickr-weekday'>")+`
      </span>
      `}}function Ct(){e.calendarContainer.classList.add("hasWeeks");var o=B("div","flatpickr-weekwrapper");o.appendChild(B("span","flatpickr-weekday",e.l10n.weekAbbreviation));var s=B("div","flatpickr-weeks");return o.appendChild(s),{weekWrapper:o,weekNumbers:s}}function Ae(o,s){s===void 0&&(s=!0);var f=s?o:o-e.currentMonth;f<0&&e._hidePrevMonthArrow===!0||f>0&&e._hideNextMonthArrow===!0||(e.currentMonth+=f,(e.currentMonth<0||e.currentMonth>11)&&(e.currentYear+=e.currentMonth>11?1:-1,e.currentMonth=(e.currentMonth+12)%12,H("onYearChange"),De()),Ve(),H("onMonthChange"),nn())}function We(o,s){if(o===void 0&&(o=!0),s===void 0&&(s=!0),e.input.value="",e.altInput!==void 0&&(e.altInput.value=""),e.mobileInput!==void 0&&(e.mobileInput.value=""),e.selectedDates=[],e.latestSelectedDateObj=void 0,s===!0&&(e.currentYear=e._initialDate.getFullYear(),e.currentMonth=e._initialDate.getMonth()),e.config.enableTime===!0){var f=aa(e.config),v=f.hours,w=f.minutes,T=f.seconds;O(v,w,T)}e.redraw(),o&&H("onChange")}function Ke(){e.isOpen=!1,e.isMobile||(e.calendarContainer!==void 0&&e.calendarContainer.classList.remove("open"),e._input!==void 0&&e._input.classList.remove("active")),H("onClose")}function wt(){e.config!==void 0&&H("onDestroy");for(var o=e._handlers.length;o--;)e._handlers[o].remove();if(e._handlers=[],e.mobileInput)e.mobileInput.parentNode&&e.mobileInput.parentNode.removeChild(e.mobileInput),e.mobileInput=void 0;else if(e.calendarContainer&&e.calendarContainer.parentNode)if(e.config.static&&e.calendarContainer.parentNode){var s=e.calendarContainer.parentNode;if(s.lastChild&&s.removeChild(s.lastChild),s.parentNode){for(;s.firstChild;)s.parentNode.insertBefore(s.firstChild,s);s.parentNode.removeChild(s)}}else e.calendarContainer.parentNode.removeChild(e.calendarContainer);e.altInput&&(e.input.type="text",e.altInput.parentNode&&e.altInput.parentNode.removeChild(e.altInput),delete e.altInput),e.input&&(e.input.type=e.input._type,e.input.classList.remove("flatpickr-input"),e.input.removeAttribute("readonly")),["_showTimeInput","latestSelectedDateObj","_hideNextMonthArrow","_hidePrevMonthArrow","__hideNextMonthArrow","__hidePrevMonthArrow","isMobile","isOpen","selectedDateElem","minDateHasTime","maxDateHasTime","days","daysContainer","_input","_positionElement","innerContainer","rContainer","monthNav","todayDateElem","calendarContainer","weekdayContainer","prevMonthNav","nextMonthNav","monthsDropdownContainer","currentMonthElement","currentYearElement","navigationCurrentMonth","selectedDateElem","config"].forEach(function(f){try{delete e[f]}catch{}})}function J(o){return e.calendarContainer.contains(o)}function gn(o){if(e.isOpen&&!e.config.inline){var s=ae(o),f=J(s),v=s===e.input||s===e.altInput||e.element.contains(s)||o.path&&o.path.indexOf&&(~o.path.indexOf(e.input)||~o.path.indexOf(e.altInput)),w=!v&&!f&&!J(o.relatedTarget),T=!e.config.ignoredFocusElements.some(function(F){return F.contains(s)});w&&T&&(e.config.allowInput&&e.setDate(e._input.value,!1,e.config.altInput?e.config.altFormat:e.config.dateFormat),e.timeContainer!==void 0&&e.minuteElement!==void 0&&e.hourElement!==void 0&&e.input.value!==""&&e.input.value!==void 0&&C(),e.close(),e.config&&e.config.mode==="range"&&e.selectedDates.length===1&&e.clear(!1))}}function ze(o){if(!(!o||e.config.minDate&&o<e.config.minDate.getFullYear()||e.config.maxDate&&o>e.config.maxDate.getFullYear())){var s=o,f=e.currentYear!==s;e.currentYear=s||e.currentYear,e.config.maxDate&&e.currentYear===e.config.maxDate.getFullYear()?e.currentMonth=Math.min(e.config.maxDate.getMonth(),e.currentMonth):e.config.minDate&&e.currentYear===e.config.minDate.getFullYear()&&(e.currentMonth=Math.max(e.config.minDate.getMonth(),e.currentMonth)),f&&(e.redraw(),H("onYearChange"),De())}}function ye(o,s){var f;s===void 0&&(s=!0);var v=e.parseDate(o,void 0,s);if(e.config.minDate&&v&&ie(v,e.config.minDate,s!==void 0?s:!e.minDateHasTime)<0||e.config.maxDate&&v&&ie(v,e.config.maxDate,s!==void 0?s:!e.maxDateHasTime)>0)return!1;if(!e.config.enable&&e.config.disable.length===0)return!0;if(v===void 0)return!1;for(var w=!!e.config.enable,T=(f=e.config.enable)!==null&&f!==void 0?f:e.config.disable,F=0,I=void 0;F<T.length;F++){if(I=T[F],typeof I=="function"&&I(v))return w;if(I instanceof Date&&v!==void 0&&I.getTime()===v.getTime())return w;if(typeof I=="string"){var P=e.parseDate(I,void 0,!0);return P&&P.getTime()===v.getTime()?w:!w}else if(typeof I=="object"&&v!==void 0&&I.from&&I.to&&v.getTime()>=I.from.getTime()&&v.getTime()<=I.to.getTime())return w}return!w}function Ge(o){return e.daysContainer!==void 0?o.className.indexOf("hidden")===-1&&o.className.indexOf("flatpickr-disabled")===-1&&e.daysContainer.contains(o):!1}function Dt(o){var s=o.target===e._input,f=e._input.value.trimEnd()!==yn();s&&f&&!(o.relatedTarget&&J(o.relatedTarget))&&e.setDate(e._input.value,!0,o.target===e.altInput?e.config.altFormat:e.config.dateFormat)}function vn(o){var s=ae(o),f=e.config.wrap?t.contains(s):s===e._input,v=e.config.allowInput,w=e.isOpen&&(!v||!f),T=e.config.inline&&f&&!v;if(o.keyCode===13&&f){if(v)return e.setDate(e._input.value,!0,s===e.altInput?e.config.altFormat:e.config.dateFormat),e.close(),s.blur();e.open()}else if(J(s)||w||T){var F=!!e.timeContainer&&e.timeContainer.contains(s);switch(o.keyCode){case 13:F?(o.preventDefault(),C(),Xe()):Kn(o);break;case 27:o.preventDefault(),Xe();break;case 8:case 46:f&&!e.config.allowInput&&(o.preventDefault(),e.clear());break;case 37:case 39:if(!F&&!f){o.preventDefault();var I=h();if(e.daysContainer!==void 0&&(v===!1||I&&Ge(I))){var P=o.keyCode===39?1:-1;o.ctrlKey?(o.stopPropagation(),Ae(P),ke(ge(1),0)):ke(void 0,P)}}else e.hourElement&&e.hourElement.focus();break;case 38:case 40:o.preventDefault();var $=o.keyCode===40?1:-1;e.daysContainer&&s.$i!==void 0||s===e.input||s===e.altInput?o.ctrlKey?(o.stopPropagation(),ze(e.currentYear-$),ke(ge(1),0)):F||ke(void 0,$*7):s===e.currentYearElement?ze(e.currentYear-$):e.config.enableTime&&(!F&&e.hourElement&&e.hourElement.focus(),C(o),e._debouncedChange());break;case 9:if(F){var x=[e.hourElement,e.minuteElement,e.secondElement,e.amPM].concat(e.pluginElements).filter(function(X){return X}),R=x.indexOf(s);if(R!==-1){var oe=x[R+(o.shiftKey?-1:1)];o.preventDefault(),(oe||e._input).focus()}}else!e.config.noCalendar&&e.daysContainer&&e.daysContainer.contains(s)&&o.shiftKey&&(o.preventDefault(),e._input.focus());break}}if(e.amPM!==void 0&&s===e.amPM)switch(o.key){case e.l10n.amPM[0].charAt(0):case e.l10n.amPM[0].charAt(0).toLowerCase():e.amPM.textContent=e.l10n.amPM[0],A(),de();break;case e.l10n.amPM[1].charAt(0):case e.l10n.amPM[1].charAt(0).toLowerCase():e.amPM.textContent=e.l10n.amPM[1],A(),de();break}(f||J(s))&&H("onKeyDown",o)}function Qe(o,s){if(s===void 0&&(s="flatpickr-day"),!(e.selectedDates.length!==1||o&&(!o.classList.contains(s)||o.classList.contains("flatpickr-disabled")))){for(var f=o?o.dateObj.getTime():e.days.firstElementChild.dateObj.getTime(),v=e.parseDate(e.selectedDates[0],void 0,!0).getTime(),w=Math.min(f,e.selectedDates[0].getTime()),T=Math.max(f,e.selectedDates[0].getTime()),F=!1,I=0,P=0,$=w;$<T;$+=ws.DAY)ye(new Date($),!0)||(F=F||$>w&&$<T,$<v&&(!I||$>I)?I=$:$>v&&(!P||$<P)&&(P=$));var x=Array.from(e.rContainer.querySelectorAll("*:nth-child(-n+"+e.config.showMonths+") > ."+s));x.forEach(function(R){var oe=R.dateObj,X=oe.getTime(),Fe=I>0&&X<I||P>0&&X>P;if(Fe){R.classList.add("notAllowed"),["inRange","startRange","endRange"].forEach(function(Ie){R.classList.remove(Ie)});return}else if(F&&!Fe)return;["startRange","inRange","endRange","notAllowed"].forEach(function(Ie){R.classList.remove(Ie)}),o!==void 0&&(o.classList.add(f<=e.selectedDates[0].getTime()?"startRange":"endRange"),v<f&&X===v?R.classList.add("startRange"):v>f&&X===v&&R.classList.add("endRange"),X>=I&&(P===0||X<=P)&&bs(X,v,f)&&R.classList.add("inRange"))})}}function St(){e.isOpen&&!e.config.static&&!e.config.inline&&ce()}function At(o,s){if(s===void 0&&(s=e._positionElement),e.isMobile===!0){if(o){o.preventDefault();var f=ae(o);f&&f.blur()}e.mobileInput!==void 0&&(e.mobileInput.focus(),e.mobileInput.click()),H("onOpen");return}else if(e._input.disabled||e.config.inline)return;var v=e.isOpen;e.isOpen=!0,v||(e.calendarContainer.classList.add("open"),e._input.classList.add("active"),H("onOpen"),ce(s)),e.config.enableTime===!0&&e.config.noCalendar===!0&&e.config.allowInput===!1&&(o===void 0||!e.timeContainer.contains(o.relatedTarget))&&setTimeout(function(){return e.hourElement.select()},50)}function Je(o){return function(s){var f=e.config["_"+o+"Date"]=e.parseDate(s,e.config.dateFormat),v=e.config["_"+(o==="min"?"max":"min")+"Date"];f!==void 0&&(e[o==="min"?"minDateHasTime":"maxDateHasTime"]=f.getHours()>0||f.getMinutes()>0||f.getSeconds()>0),e.selectedDates&&(e.selectedDates=e.selectedDates.filter(function(w){return ye(w)}),!e.selectedDates.length&&o==="min"&&N(f),de()),e.daysContainer&&(z(),f!==void 0?e.currentYearElement[o]=f.getFullYear().toString():e.currentYearElement.removeAttribute(o),e.currentYearElement.disabled=!!v&&f!==void 0&&v.getFullYear()===f.getFullYear())}}function Tt(){var o=["wrap","weekNumbers","allowInput","allowInvalidPreload","clickOpens","time_24hr","enableTime","noCalendar","altInput","shorthandCurrentMonth","inline","static","enableSeconds","disableMobile"],s=Q(Q({},JSON.parse(JSON.stringify(t.dataset||{}))),i),f={};e.config.parseDate=s.parseDate,e.config.formatDate=s.formatDate,Object.defineProperty(e.config,"enable",{get:function(){return e.config._enable},set:function(x){e.config._enable=Gn(x)}}),Object.defineProperty(e.config,"disable",{get:function(){return e.config._disable},set:function(x){e.config._disable=Gn(x)}});var v=s.mode==="time";if(!s.dateFormat&&(s.enableTime||v)){var w=q.defaultConfig.dateFormat||un.dateFormat;f.dateFormat=s.noCalendar||v?"H:i"+(s.enableSeconds?":S":""):w+" H:i"+(s.enableSeconds?":S":"")}if(s.altInput&&(s.enableTime||v)&&!s.altFormat){var T=q.defaultConfig.altFormat||un.altFormat;f.altFormat=s.noCalendar||v?"h:i"+(s.enableSeconds?":S K":" K"):T+(" h:i"+(s.enableSeconds?":S":"")+" K")}Object.defineProperty(e.config,"minDate",{get:function(){return e.config._minDate},set:Je("min")}),Object.defineProperty(e.config,"maxDate",{get:function(){return e.config._maxDate},set:Je("max")});var F=function(x){return function(R){e.config[x==="min"?"_minTime":"_maxTime"]=e.parseDate(R,"H:i:S")}};Object.defineProperty(e.config,"minTime",{get:function(){return e.config._minTime},set:F("min")}),Object.defineProperty(e.config,"maxTime",{get:function(){return e.config._maxTime},set:F("max")}),s.mode==="time"&&(e.config.noCalendar=!0,e.config.enableTime=!0),Object.assign(e.config,f,s);for(var I=0;I<o.length;I++)e.config[o[I]]=e.config[o[I]]===!0||e.config[o[I]]==="true";Zt.filter(function(x){return e.config[x]!==void 0}).forEach(function(x){e.config[x]=ea(e.config[x]||[]).map(a)}),e.isMobile=!e.config.disableMobile&&!e.config.inline&&e.config.mode==="single"&&!e.config.disable.length&&!e.config.enable&&!e.config.weekNumbers&&/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);for(var I=0;I<e.config.plugins.length;I++){var P=e.config.plugins[I](e)||{};for(var $ in P)Zt.indexOf($)>-1?e.config[$]=ea(P[$]).map(a).concat(e.config[$]):typeof s[$]>"u"&&(e.config[$]=P[$])}s.altInputClass||(e.config.altInputClass=_n().className+" "+e.config.altInputClass),H("onParseConfig")}function _n(){return e.config.wrap?t.querySelector("[data-input]"):t}function Te(){typeof e.config.locale!="object"&&typeof q.l10ns[e.config.locale]>"u"&&e.config.errorHandler(new Error("flatpickr: invalid locale "+e.config.locale)),e.l10n=Q(Q({},q.l10ns.default),typeof e.config.locale=="object"?e.config.locale:e.config.locale!=="default"?q.l10ns[e.config.locale]:void 0),Ye.D="("+e.l10n.weekdays.shorthand.join("|")+")",Ye.l="("+e.l10n.weekdays.longhand.join("|")+")",Ye.M="("+e.l10n.months.shorthand.join("|")+")",Ye.F="("+e.l10n.months.longhand.join("|")+")",Ye.K="("+e.l10n.amPM[0]+"|"+e.l10n.amPM[1]+"|"+e.l10n.amPM[0].toLowerCase()+"|"+e.l10n.amPM[1].toLowerCase()+")";var o=Q(Q({},i),JSON.parse(JSON.stringify(t.dataset||{})));o.time_24hr===void 0&&q.defaultConfig.time_24hr===void 0&&(e.config.time_24hr=e.l10n.time_24hr),e.formatDate=Ei(e),e.parseDate=sa({config:e.config,l10n:e.l10n})}function ce(o){if(typeof e.config.position=="function")return void e.config.position(e,o);if(e.calendarContainer!==void 0){H("onPreCalendarPosition");var s=o||e._positionElement,f=Array.prototype.reduce.call(e.calendarContainer.children,(function(Ce,Pe){return Ce+Pe.offsetHeight}),0),v=e.calendarContainer.offsetWidth,w=e.config.position.split(" "),T=w[0],F=w.length>1?w[1]:null,I=s.getBoundingClientRect(),P=window.innerHeight-I.bottom,$=T==="above"||T!=="below"&&P<f&&I.top>f,x=window.pageYOffset+I.top+($?-f-2:s.offsetHeight+2);if(Z(e.calendarContainer,"arrowTop",!$),Z(e.calendarContainer,"arrowBottom",$),!e.config.inline){var R=window.pageXOffset+I.left,oe=!1,X=!1;F==="center"?(R-=(v-I.width)/2,oe=!0):F==="right"&&(R-=v-I.width,X=!0),Z(e.calendarContainer,"arrowLeft",!oe&&!X),Z(e.calendarContainer,"arrowCenter",oe),Z(e.calendarContainer,"arrowRight",X);var Fe=window.document.body.offsetWidth-(window.pageXOffset+I.right),Ie=R+v>window.document.body.offsetWidth,Lt=Fe+v>window.document.body.offsetWidth;if(Z(e.calendarContainer,"rightMost",Ie),!e.config.static)if(e.calendarContainer.style.top=x+"px",!Ie)e.calendarContainer.style.left=R+"px",e.calendarContainer.style.right="auto";else if(!Lt)e.calendarContainer.style.left="auto",e.calendarContainer.style.right=Fe+"px";else{var bn=$t();if(bn===void 0)return;var Cn=window.document.body.offsetWidth,Ft=Math.max(0,Cn/2-v/2),Xn=".flatpickr-calendar.centerMost:before",Oe=".flatpickr-calendar.centerMost:after",Ne=bn.cssRules.length,Pt="{left:"+I.left+"px;right:auto;}";Z(e.calendarContainer,"rightMost",!1),Z(e.calendarContainer,"centerMost",!0),bn.insertRule(Xn+","+Oe+Pt,Ne),e.calendarContainer.style.left=Ft+"px",e.calendarContainer.style.right="auto"}}}}function $t(){for(var o=null,s=0;s<document.styleSheets.length;s++){var f=document.styleSheets[s];if(f.cssRules){try{f.cssRules}catch{continue}o=f;break}}return o??Le()}function Le(){var o=document.createElement("style");return document.head.appendChild(o),o.sheet}function z(){e.config.noCalendar||e.isMobile||(De(),nn(),Ve())}function Xe(){e._input.focus(),window.navigator.userAgent.indexOf("MSIE")!==-1||navigator.msMaxTouchPoints!==void 0?setTimeout(e.close,0):e.close()}function Kn(o){o.preventDefault(),o.stopPropagation();var s=function(x){return x.classList&&x.classList.contains("flatpickr-day")&&!x.classList.contains("flatpickr-disabled")&&!x.classList.contains("notAllowed")},f=_i(ae(o),s);if(f!==void 0){var v=f,w=e.latestSelectedDateObj=new Date(v.dateObj.getTime()),T=(w.getMonth()<e.currentMonth||w.getMonth()>e.currentMonth+e.config.showMonths-1)&&e.config.mode!=="range";if(e.selectedDateElem=v,e.config.mode==="single")e.selectedDates=[w];else if(e.config.mode==="multiple"){var F=$e(w);F?e.selectedDates.splice(parseInt(F),1):e.selectedDates.push(w)}else e.config.mode==="range"&&(e.selectedDates.length===2&&e.clear(!1,!1),e.latestSelectedDateObj=w,e.selectedDates.push(w),ie(w,e.selectedDates[0],!0)!==0&&e.selectedDates.sort(function(x,R){return x.getTime()-R.getTime()}));if(A(),T){var I=e.currentYear!==w.getFullYear();e.currentYear=w.getFullYear(),e.currentMonth=w.getMonth(),I&&(H("onYearChange"),De()),H("onMonthChange")}if(nn(),Ve(),de(),!T&&e.config.mode!=="range"&&e.config.showMonths===1?ue(v):e.selectedDateElem!==void 0&&e.hourElement===void 0&&e.selectedDateElem&&e.selectedDateElem.focus(),e.hourElement!==void 0&&e.hourElement!==void 0&&e.hourElement.focus(),e.config.closeOnSelect){var P=e.config.mode==="single"&&!e.config.enableTime,$=e.config.mode==="range"&&e.selectedDates.length===2&&!e.config.enableTime;(P||$)&&Xe()}V()}}var Ze={locale:[Te,Se],showMonths:[Wn,E,Ee],minDate:[Y],maxDate:[Y],positionElement:[Qn],clickOpens:[function(){e.config.clickOpens===!0?(M(e._input,"focus",e.open),M(e._input,"click",e.open)):(e._input.removeEventListener("focus",e.open),e._input.removeEventListener("click",e.open))}]};function It(o,s){if(o!==null&&typeof o=="object"){Object.assign(e.config,o);for(var f in o)Ze[f]!==void 0&&Ze[f].forEach(function(v){return v()})}else e.config[o]=s,Ze[o]!==void 0?Ze[o].forEach(function(v){return v()}):Zt.indexOf(o)>-1&&(e.config[o]=ea(s));e.redraw(),de(!0)}function zn(o,s){var f=[];if(o instanceof Array)f=o.map(function(v){return e.parseDate(v,s)});else if(o instanceof Date||typeof o=="number")f=[e.parseDate(o,s)];else if(typeof o=="string")switch(e.config.mode){case"single":case"time":f=[e.parseDate(o,s)];break;case"multiple":f=o.split(e.config.conjunction).map(function(v){return e.parseDate(v,s)});break;case"range":f=o.split(e.l10n.rangeSeparator).map(function(v){return e.parseDate(v,s)});break}else e.config.errorHandler(new Error("Invalid date supplied: "+JSON.stringify(o)));e.selectedDates=e.config.allowInvalidPreload?f:f.filter(function(v){return v instanceof Date&&ye(v,!1)}),e.config.mode==="range"&&e.selectedDates.sort(function(v,w){return v.getTime()-w.getTime()})}function Ot(o,s,f){if(s===void 0&&(s=!1),f===void 0&&(f=e.config.dateFormat),o!==0&&!o||o instanceof Array&&o.length===0)return e.clear(s);zn(o,f),e.latestSelectedDateObj=e.selectedDates[e.selectedDates.length-1],e.redraw(),Y(void 0,s),N(),e.selectedDates.length===0&&e.clear(!1),de(s),s&&H("onChange")}function Gn(o){return o.slice().map(function(s){return typeof s=="string"||typeof s=="number"||s instanceof Date?e.parseDate(s,void 0,!0):s&&typeof s=="object"&&s.from&&s.to?{from:e.parseDate(s.from,void 0),to:e.parseDate(s.to,void 0)}:s}).filter(function(s){return s})}function be(){e.selectedDates=[],e.now=e.parseDate(e.config.now)||new Date;var o=e.config.defaultDate||((e.input.nodeName==="INPUT"||e.input.nodeName==="TEXTAREA")&&e.input.placeholder&&e.input.value===e.input.placeholder?null:e.input.value);o&&zn(o,e.config.dateFormat),e._initialDate=e.selectedDates.length>0?e.selectedDates[0]:e.config.minDate&&e.config.minDate.getTime()>e.now.getTime()?e.config.minDate:e.config.maxDate&&e.config.maxDate.getTime()<e.now.getTime()?e.config.maxDate:e.now,e.currentYear=e._initialDate.getFullYear(),e.currentMonth=e._initialDate.getMonth(),e.selectedDates.length>0&&(e.latestSelectedDateObj=e.selectedDates[0]),e.config.minTime!==void 0&&(e.config.minTime=e.parseDate(e.config.minTime,"H:i")),e.config.maxTime!==void 0&&(e.config.maxTime=e.parseDate(e.config.maxTime,"H:i")),e.minDateHasTime=!!e.config.minDate&&(e.config.minDate.getHours()>0||e.config.minDate.getMinutes()>0||e.config.minDate.getSeconds()>0),e.maxDateHasTime=!!e.config.maxDate&&(e.config.maxDate.getHours()>0||e.config.maxDate.getMinutes()>0||e.config.maxDate.getSeconds()>0)}function Nt(){if(e.input=_n(),!e.input){e.config.errorHandler(new Error("Invalid input element specified"));return}e.input._type=e.input.type,e.input.type="text",e.input.classList.add("flatpickr-input"),e._input=e.input,e.config.altInput&&(e.altInput=B(e.input.nodeName,e.config.altInputClass),e._input=e.altInput,e.altInput.placeholder=e.input.placeholder,e.altInput.disabled=e.input.disabled,e.altInput.required=e.input.required,e.altInput.tabIndex=e.input.tabIndex,e.altInput.type="text",e.input.setAttribute("type","hidden"),!e.config.static&&e.input.parentNode&&e.input.parentNode.insertBefore(e.altInput,e.input.nextSibling)),e.config.allowInput||e._input.setAttribute("readonly","readonly"),Qn()}function Qn(){e._positionElement=e.config.positionElement||e._input}function Mt(){var o=e.config.enableTime?e.config.noCalendar?"time":"datetime-local":"date";e.mobileInput=B("input",e.input.className+" flatpickr-mobile"),e.mobileInput.tabIndex=1,e.mobileInput.type=o,e.mobileInput.disabled=e.input.disabled,e.mobileInput.required=e.input.required,e.mobileInput.placeholder=e.input.placeholder,e.mobileFormatStr=o==="datetime-local"?"Y-m-d\\TH:i:S":o==="date"?"Y-m-d":"H:i:S",e.selectedDates.length>0&&(e.mobileInput.defaultValue=e.mobileInput.value=e.formatDate(e.selectedDates[0],e.mobileFormatStr)),e.config.minDate&&(e.mobileInput.min=e.formatDate(e.config.minDate,"Y-m-d")),e.config.maxDate&&(e.mobileInput.max=e.formatDate(e.config.maxDate,"Y-m-d")),e.input.getAttribute("step")&&(e.mobileInput.step=String(e.input.getAttribute("step"))),e.input.type="hidden",e.altInput!==void 0&&(e.altInput.type="hidden");try{e.input.parentNode&&e.input.parentNode.insertBefore(e.mobileInput,e.input.nextSibling)}catch{}M(e.mobileInput,"change",function(s){e.setDate(ae(s).value,!1,e.mobileFormatStr),H("onChange"),H("onClose")})}function xt(o){if(e.isOpen===!0)return e.close();e.open(o)}function H(o,s){if(e.config!==void 0){var f=e.config[o];if(f!==void 0&&f.length>0)for(var v=0;f[v]&&v<f.length;v++)f[v](e.selectedDates,e.input.value,e,s);o==="onChange"&&(e.input.dispatchEvent(En("change")),e.input.dispatchEvent(En("input")))}}function En(o){var s=document.createEvent("Event");return s.initEvent(o,!0,!0),s}function $e(o){for(var s=0;s<e.selectedDates.length;s++){var f=e.selectedDates[s];if(f instanceof Date&&ie(f,o)===0)return""+s}return!1}function en(o){return e.config.mode!=="range"||e.selectedDates.length<2?!1:ie(o,e.selectedDates[0])>=0&&ie(o,e.selectedDates[1])<=0}function nn(){e.config.noCalendar||e.isMobile||!e.monthNav||(e.yearElements.forEach(function(o,s){var f=new Date(e.currentYear,e.currentMonth,1);f.setMonth(e.currentMonth+s),e.config.showMonths>1||e.config.monthSelectorType==="static"?e.monthElements[s].textContent=gt(f.getMonth(),e.config.shorthandCurrentMonth,e.l10n)+" ":e.monthsDropdownContainer.value=f.getMonth().toString(),o.value=f.getFullYear().toString()}),e._hidePrevMonthArrow=e.config.minDate!==void 0&&(e.currentYear===e.config.minDate.getFullYear()?e.currentMonth<=e.config.minDate.getMonth():e.currentYear<e.config.minDate.getFullYear()),e._hideNextMonthArrow=e.config.maxDate!==void 0&&(e.currentYear===e.config.maxDate.getFullYear()?e.currentMonth+1>e.config.maxDate.getMonth():e.currentYear>e.config.maxDate.getFullYear()))}function yn(o){var s=o||(e.config.altInput?e.config.altFormat:e.config.dateFormat);return e.selectedDates.map(function(f){return e.formatDate(f,s)}).filter(function(f,v,w){return e.config.mode!=="range"||e.config.enableTime||w.indexOf(f)===v}).join(e.config.mode!=="range"?e.config.conjunction:e.l10n.rangeSeparator)}function de(o){o===void 0&&(o=!0),e.mobileInput!==void 0&&e.mobileFormatStr&&(e.mobileInput.value=e.latestSelectedDateObj!==void 0?e.formatDate(e.latestSelectedDateObj,e.mobileFormatStr):""),e.input.value=yn(e.config.dateFormat),e.altInput!==void 0&&(e.altInput.value=yn(e.config.altFormat)),o!==!1&&H("onValueUpdate")}function Jn(o){var s=ae(o),f=e.prevMonthNav.contains(s),v=e.nextMonthNav.contains(s);f||v?Ae(f?-1:1):e.yearElements.indexOf(s)>=0?s.select():s.classList.contains("arrowUp")?e.changeYear(e.currentYear+1):s.classList.contains("arrowDown")&&e.changeYear(e.currentYear-1)}function kt(o){o.preventDefault();var s=o.type==="keydown",f=ae(o),v=f;e.amPM!==void 0&&f===e.amPM&&(e.amPM.textContent=e.l10n.amPM[se(e.amPM.textContent===e.l10n.amPM[0])]);var w=parseFloat(v.getAttribute("min")),T=parseFloat(v.getAttribute("max")),F=parseFloat(v.getAttribute("step")),I=parseInt(v.value,10),P=o.delta||(s?o.which===38?1:-1:0),$=I+F*P;if(typeof v.value<"u"&&v.value.length===2){var x=v===e.hourElement,R=v===e.minuteElement;$<w?($=T+$+se(!x)+(se(x)&&se(!e.amPM)),R&&D(void 0,-1,e.hourElement)):$>T&&($=v===e.hourElement?$-T-se(!e.amPM):w,R&&D(void 0,1,e.hourElement)),e.amPM&&x&&(F===1?$+I===23:Math.abs($-I)>F)&&(e.amPM.textContent=e.l10n.amPM[se(e.amPM.textContent===e.l10n.amPM[0])]),v.value=ne($)}}return m(),e}function cn(t,i){for(var e=Array.prototype.slice.call(t).filter(function(a){return a instanceof HTMLElement}),d=[],m=0;m<e.length;m++){var h=e[m];try{if(h.getAttribute("data-fp-omit")!==null)continue;h._flatpickr!==void 0&&(h._flatpickr.destroy(),h._flatpickr=void 0),h._flatpickr=Ss(h,i||{}),d.push(h._flatpickr)}catch(a){console.error(a)}}return d.length===1?d[0]:d}typeof HTMLElement<"u"&&typeof HTMLCollection<"u"&&typeof NodeList<"u"&&(HTMLCollection.prototype.flatpickr=NodeList.prototype.flatpickr=function(t){return cn(this,t)},HTMLElement.prototype.flatpickr=function(t){return cn([this],t)});var q=function(t,i){return typeof t=="string"?cn(window.document.querySelectorAll(t),i):t instanceof Node?cn([t],i):cn(t,i)};q.defaultConfig={};q.l10ns={en:Q({},Hn),default:Q({},Hn)};q.localize=function(t){q.l10ns.default=Q(Q({},q.l10ns.default),t)};q.setDefaults=function(t){q.defaultConfig=Q(Q({},q.defaultConfig),t)};q.parseDate=sa({});q.formatDate=Ei({});q.compareDates=ie;typeof jQuery<"u"&&typeof jQuery.fn<"u"&&(jQuery.fn.flatpickr=function(t){return cn(this,t)});Date.prototype.fp_incr=function(t){return new Date(this.getFullYear(),this.getMonth(),this.getDate()+(typeof t=="string"?parseInt(t,10):t))};typeof window<"u"&&(window.flatpickr=q);function As(){q(".datepicker",{allowInput:!0})}const Ts=`/*!
 * Select2 4.1.0-rc.0
 * https://select2.github.io
 *
 * Released under the MIT license
 * https://github.com/select2/select2/blob/master/LICENSE.md
 */
;(function (factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD. Register as an anonymous module.
    define(['jquery'], factory);
  } else if (typeof module === 'object' && module.exports) {
    // Node/CommonJS
    module.exports = function (root, jQuery) {
      if (jQuery === undefined) {
        // require('jQuery') returns a factory that requires window to
        // build a jQuery instance, we normalize how we use modules
        // that require this pattern but the window provided is a noop
        // if it's defined (how jquery works)
        if (typeof window !== 'undefined') {
          jQuery = require('jquery');
        }
        else {
          jQuery = require('jquery')(root);
        }
      }
      factory(jQuery);
      return jQuery;
    };
  } else {
    // Browser globals
    factory(jQuery);
  }
} (function (jQuery) {
  // This is needed so we can catch the AMD loader configuration and use it
  // The inner file should be wrapped (by \`banner.start.js\`) in a function that
  // returns the AMD loader references.
  var S2 =(function () {
  // Restore the Select2 AMD loader so it can be used
  // Needed mostly in the language files, where the loader is not inserted
  if (jQuery && jQuery.fn && jQuery.fn.select2 && jQuery.fn.select2.amd) {
    var S2 = jQuery.fn.select2.amd;
  }
var S2;(function () { if (!S2 || !S2.requirejs) {
if (!S2) { S2 = {}; } else { require = S2; }
/**
 * @license almond 0.3.3 Copyright jQuery Foundation and other contributors.
 * Released under MIT license, http://github.com/requirejs/almond/LICENSE
 */
//Going sloppy to avoid 'use strict' string cost, but strict practices should
//be followed.
/*global setTimeout: false */

var requirejs, require, define;
(function (undef) {
    var main, req, makeMap, handlers,
        defined = {},
        waiting = {},
        config = {},
        defining = {},
        hasOwn = Object.prototype.hasOwnProperty,
        aps = [].slice,
        jsSuffixRegExp = /\\.js$/;

    function hasProp(obj, prop) {
        return hasOwn.call(obj, prop);
    }

    /**
     * Given a relative module name, like ./something, normalize it to
     * a real name that can be mapped to a path.
     * @param {String} name the relative name
     * @param {String} baseName a real name that the name arg is relative
     * to.
     * @returns {String} normalized name
     */
    function normalize(name, baseName) {
        var nameParts, nameSegment, mapValue, foundMap, lastIndex,
            foundI, foundStarMap, starI, i, j, part, normalizedBaseParts,
            baseParts = baseName && baseName.split("/"),
            map = config.map,
            starMap = (map && map['*']) || {};

        //Adjust any relative paths.
        if (name) {
            name = name.split('/');
            lastIndex = name.length - 1;

            // If wanting node ID compatibility, strip .js from end
            // of IDs. Have to do this here, and not in nameToUrl
            // because node allows either .js or non .js to map
            // to same file.
            if (config.nodeIdCompat && jsSuffixRegExp.test(name[lastIndex])) {
                name[lastIndex] = name[lastIndex].replace(jsSuffixRegExp, '');
            }

            // Starts with a '.' so need the baseName
            if (name[0].charAt(0) === '.' && baseParts) {
                //Convert baseName to array, and lop off the last part,
                //so that . matches that 'directory' and not name of the baseName's
                //module. For instance, baseName of 'one/two/three', maps to
                //'one/two/three.js', but we want the directory, 'one/two' for
                //this normalization.
                normalizedBaseParts = baseParts.slice(0, baseParts.length - 1);
                name = normalizedBaseParts.concat(name);
            }

            //start trimDots
            for (i = 0; i < name.length; i++) {
                part = name[i];
                if (part === '.') {
                    name.splice(i, 1);
                    i -= 1;
                } else if (part === '..') {
                    // If at the start, or previous value is still ..,
                    // keep them so that when converted to a path it may
                    // still work when converted to a path, even though
                    // as an ID it is less than ideal. In larger point
                    // releases, may be better to just kick out an error.
                    if (i === 0 || (i === 1 && name[2] === '..') || name[i - 1] === '..') {
                        continue;
                    } else if (i > 0) {
                        name.splice(i - 1, 2);
                        i -= 2;
                    }
                }
            }
            //end trimDots

            name = name.join('/');
        }

        //Apply map config if available.
        if ((baseParts || starMap) && map) {
            nameParts = name.split('/');

            for (i = nameParts.length; i > 0; i -= 1) {
                nameSegment = nameParts.slice(0, i).join("/");

                if (baseParts) {
                    //Find the longest baseName segment match in the config.
                    //So, do joins on the biggest to smallest lengths of baseParts.
                    for (j = baseParts.length; j > 0; j -= 1) {
                        mapValue = map[baseParts.slice(0, j).join('/')];

                        //baseName segment has  config, find if it has one for
                        //this name.
                        if (mapValue) {
                            mapValue = mapValue[nameSegment];
                            if (mapValue) {
                                //Match, update name to the new value.
                                foundMap = mapValue;
                                foundI = i;
                                break;
                            }
                        }
                    }
                }

                if (foundMap) {
                    break;
                }

                //Check for a star map match, but just hold on to it,
                //if there is a shorter segment match later in a matching
                //config, then favor over this star map.
                if (!foundStarMap && starMap && starMap[nameSegment]) {
                    foundStarMap = starMap[nameSegment];
                    starI = i;
                }
            }

            if (!foundMap && foundStarMap) {
                foundMap = foundStarMap;
                foundI = starI;
            }

            if (foundMap) {
                nameParts.splice(0, foundI, foundMap);
                name = nameParts.join('/');
            }
        }

        return name;
    }

    function makeRequire(relName, forceSync) {
        return function () {
            //A version of a require function that passes a moduleName
            //value for items that may need to
            //look up paths relative to the moduleName
            var args = aps.call(arguments, 0);

            //If first arg is not require('string'), and there is only
            //one arg, it is the array form without a callback. Insert
            //a null so that the following concat is correct.
            if (typeof args[0] !== 'string' && args.length === 1) {
                args.push(null);
            }
            return req.apply(undef, args.concat([relName, forceSync]));
        };
    }

    function makeNormalize(relName) {
        return function (name) {
            return normalize(name, relName);
        };
    }

    function makeLoad(depName) {
        return function (value) {
            defined[depName] = value;
        };
    }

    function callDep(name) {
        if (hasProp(waiting, name)) {
            var args = waiting[name];
            delete waiting[name];
            defining[name] = true;
            main.apply(undef, args);
        }

        if (!hasProp(defined, name) && !hasProp(defining, name)) {
            throw new Error('No ' + name);
        }
        return defined[name];
    }

    //Turns a plugin!resource to [plugin, resource]
    //with the plugin being undefined if the name
    //did not have a plugin prefix.
    function splitPrefix(name) {
        var prefix,
            index = name ? name.indexOf('!') : -1;
        if (index > -1) {
            prefix = name.substring(0, index);
            name = name.substring(index + 1, name.length);
        }
        return [prefix, name];
    }

    //Creates a parts array for a relName where first part is plugin ID,
    //second part is resource ID. Assumes relName has already been normalized.
    function makeRelParts(relName) {
        return relName ? splitPrefix(relName) : [];
    }

    /**
     * Makes a name map, normalizing the name, and using a plugin
     * for normalization if necessary. Grabs a ref to plugin
     * too, as an optimization.
     */
    makeMap = function (name, relParts) {
        var plugin,
            parts = splitPrefix(name),
            prefix = parts[0],
            relResourceName = relParts[1];

        name = parts[1];

        if (prefix) {
            prefix = normalize(prefix, relResourceName);
            plugin = callDep(prefix);
        }

        //Normalize according
        if (prefix) {
            if (plugin && plugin.normalize) {
                name = plugin.normalize(name, makeNormalize(relResourceName));
            } else {
                name = normalize(name, relResourceName);
            }
        } else {
            name = normalize(name, relResourceName);
            parts = splitPrefix(name);
            prefix = parts[0];
            name = parts[1];
            if (prefix) {
                plugin = callDep(prefix);
            }
        }

        //Using ridiculous property names for space reasons
        return {
            f: prefix ? prefix + '!' + name : name, //fullName
            n: name,
            pr: prefix,
            p: plugin
        };
    };

    function makeConfig(name) {
        return function () {
            return (config && config.config && config.config[name]) || {};
        };
    }

    handlers = {
        require: function (name) {
            return makeRequire(name);
        },
        exports: function (name) {
            var e = defined[name];
            if (typeof e !== 'undefined') {
                return e;
            } else {
                return (defined[name] = {});
            }
        },
        module: function (name) {
            return {
                id: name,
                uri: '',
                exports: defined[name],
                config: makeConfig(name)
            };
        }
    };

    main = function (name, deps, callback, relName) {
        var cjsModule, depName, ret, map, i, relParts,
            args = [],
            callbackType = typeof callback,
            usingExports;

        //Use name if no relName
        relName = relName || name;
        relParts = makeRelParts(relName);

        //Call the callback to define the module, if necessary.
        if (callbackType === 'undefined' || callbackType === 'function') {
            //Pull out the defined dependencies and pass the ordered
            //values to the callback.
            //Default to [require, exports, module] if no deps
            deps = !deps.length && callback.length ? ['require', 'exports', 'module'] : deps;
            for (i = 0; i < deps.length; i += 1) {
                map = makeMap(deps[i], relParts);
                depName = map.f;

                //Fast path CommonJS standard dependencies.
                if (depName === "require") {
                    args[i] = handlers.require(name);
                } else if (depName === "exports") {
                    //CommonJS module spec 1.1
                    args[i] = handlers.exports(name);
                    usingExports = true;
                } else if (depName === "module") {
                    //CommonJS module spec 1.1
                    cjsModule = args[i] = handlers.module(name);
                } else if (hasProp(defined, depName) ||
                           hasProp(waiting, depName) ||
                           hasProp(defining, depName)) {
                    args[i] = callDep(depName);
                } else if (map.p) {
                    map.p.load(map.n, makeRequire(relName, true), makeLoad(depName), {});
                    args[i] = defined[depName];
                } else {
                    throw new Error(name + ' missing ' + depName);
                }
            }

            ret = callback ? callback.apply(defined[name], args) : undefined;

            if (name) {
                //If setting exports via "module" is in play,
                //favor that over return value and exports. After that,
                //favor a non-undefined return value over exports use.
                if (cjsModule && cjsModule.exports !== undef &&
                        cjsModule.exports !== defined[name]) {
                    defined[name] = cjsModule.exports;
                } else if (ret !== undef || !usingExports) {
                    //Use the return value from the function.
                    defined[name] = ret;
                }
            }
        } else if (name) {
            //May just be an object definition for the module. Only
            //worry about defining if have a module name.
            defined[name] = callback;
        }
    };

    requirejs = require = req = function (deps, callback, relName, forceSync, alt) {
        if (typeof deps === "string") {
            if (handlers[deps]) {
                //callback in this case is really relName
                return handlers[deps](callback);
            }
            //Just return the module wanted. In this scenario, the
            //deps arg is the module name, and second arg (if passed)
            //is just the relName.
            //Normalize module name, if it contains . or ..
            return callDep(makeMap(deps, makeRelParts(callback)).f);
        } else if (!deps.splice) {
            //deps is a config object, not an array.
            config = deps;
            if (config.deps) {
                req(config.deps, config.callback);
            }
            if (!callback) {
                return;
            }

            if (callback.splice) {
                //callback is an array, which means it is a dependency list.
                //Adjust args if there are dependencies
                deps = callback;
                callback = relName;
                relName = null;
            } else {
                deps = undef;
            }
        }

        //Support require(['a'])
        callback = callback || function () {};

        //If relName is a function, it is an errback handler,
        //so remove it.
        if (typeof relName === 'function') {
            relName = forceSync;
            forceSync = alt;
        }

        //Simulate async callback;
        if (forceSync) {
            main(undef, deps, callback, relName);
        } else {
            //Using a non-zero value because of concern for what old browsers
            //do, and latest browsers "upgrade" to 4 if lower value is used:
            //http://www.whatwg.org/specs/web-apps/current-work/multipage/timers.html#dom-windowtimers-settimeout:
            //If want a value immediately, use require('id') instead -- something
            //that works in almond on the global level, but not guaranteed and
            //unlikely to work in other AMD implementations.
            setTimeout(function () {
                main(undef, deps, callback, relName);
            }, 4);
        }

        return req;
    };

    /**
     * Just drops the config on the floor, but returns req in case
     * the config return value is used.
     */
    req.config = function (cfg) {
        return req(cfg);
    };

    /**
     * Expose module registry for debugging and tooling
     */
    requirejs._defined = defined;

    define = function (name, deps, callback) {
        if (typeof name !== 'string') {
            throw new Error('See almond README: incorrect module build, no module name');
        }

        //This module may not have dependencies
        if (!deps.splice) {
            //deps is not an array, so probably means
            //an object literal or factory function for
            //the value. Adjust args.
            callback = deps;
            deps = [];
        }

        if (!hasProp(defined, name) && !hasProp(waiting, name)) {
            waiting[name] = [name, deps, callback];
        }
    };

    define.amd = {
        jQuery: true
    };
}());

S2.requirejs = requirejs;S2.require = require;S2.define = define;
}
}());
S2.define("almond", function(){});

/* global jQuery:false, $:false */
S2.define('jquery',[],function () {
  var _$ = jQuery || $;

  if (_$ == null && console && console.error) {
    console.error(
      'Select2: An instance of jQuery or a jQuery-compatible library was not ' +
      'found. Make sure that you are including jQuery before Select2 on your ' +
      'web page.'
    );
  }

  return _$;
});

S2.define('select2/utils',[
  'jquery'
], function ($) {
  var Utils = {};

  Utils.Extend = function (ChildClass, SuperClass) {
    var __hasProp = {}.hasOwnProperty;

    function BaseConstructor () {
      this.constructor = ChildClass;
    }

    for (var key in SuperClass) {
      if (__hasProp.call(SuperClass, key)) {
        ChildClass[key] = SuperClass[key];
      }
    }

    BaseConstructor.prototype = SuperClass.prototype;
    ChildClass.prototype = new BaseConstructor();
    ChildClass.__super__ = SuperClass.prototype;

    return ChildClass;
  };

  function getMethods (theClass) {
    var proto = theClass.prototype;

    var methods = [];

    for (var methodName in proto) {
      var m = proto[methodName];

      if (typeof m !== 'function') {
        continue;
      }

      if (methodName === 'constructor') {
        continue;
      }

      methods.push(methodName);
    }

    return methods;
  }

  Utils.Decorate = function (SuperClass, DecoratorClass) {
    var decoratedMethods = getMethods(DecoratorClass);
    var superMethods = getMethods(SuperClass);

    function DecoratedClass () {
      var unshift = Array.prototype.unshift;

      var argCount = DecoratorClass.prototype.constructor.length;

      var calledConstructor = SuperClass.prototype.constructor;

      if (argCount > 0) {
        unshift.call(arguments, SuperClass.prototype.constructor);

        calledConstructor = DecoratorClass.prototype.constructor;
      }

      calledConstructor.apply(this, arguments);
    }

    DecoratorClass.displayName = SuperClass.displayName;

    function ctr () {
      this.constructor = DecoratedClass;
    }

    DecoratedClass.prototype = new ctr();

    for (var m = 0; m < superMethods.length; m++) {
      var superMethod = superMethods[m];

      DecoratedClass.prototype[superMethod] =
        SuperClass.prototype[superMethod];
    }

    var calledMethod = function (methodName) {
      // Stub out the original method if it's not decorating an actual method
      var originalMethod = function () {};

      if (methodName in DecoratedClass.prototype) {
        originalMethod = DecoratedClass.prototype[methodName];
      }

      var decoratedMethod = DecoratorClass.prototype[methodName];

      return function () {
        var unshift = Array.prototype.unshift;

        unshift.call(arguments, originalMethod);

        return decoratedMethod.apply(this, arguments);
      };
    };

    for (var d = 0; d < decoratedMethods.length; d++) {
      var decoratedMethod = decoratedMethods[d];

      DecoratedClass.prototype[decoratedMethod] = calledMethod(decoratedMethod);
    }

    return DecoratedClass;
  };

  var Observable = function () {
    this.listeners = {};
  };

  Observable.prototype.on = function (event, callback) {
    this.listeners = this.listeners || {};

    if (event in this.listeners) {
      this.listeners[event].push(callback);
    } else {
      this.listeners[event] = [callback];
    }
  };

  Observable.prototype.trigger = function (event) {
    var slice = Array.prototype.slice;
    var params = slice.call(arguments, 1);

    this.listeners = this.listeners || {};

    // Params should always come in as an array
    if (params == null) {
      params = [];
    }

    // If there are no arguments to the event, use a temporary object
    if (params.length === 0) {
      params.push({});
    }

    // Set the \`_type\` of the first object to the event
    params[0]._type = event;

    if (event in this.listeners) {
      this.invoke(this.listeners[event], slice.call(arguments, 1));
    }

    if ('*' in this.listeners) {
      this.invoke(this.listeners['*'], arguments);
    }
  };

  Observable.prototype.invoke = function (listeners, params) {
    for (var i = 0, len = listeners.length; i < len; i++) {
      listeners[i].apply(this, params);
    }
  };

  Utils.Observable = Observable;

  Utils.generateChars = function (length) {
    var chars = '';

    for (var i = 0; i < length; i++) {
      var randomChar = Math.floor(Math.random() * 36);
      chars += randomChar.toString(36);
    }

    return chars;
  };

  Utils.bind = function (func, context) {
    return function () {
      func.apply(context, arguments);
    };
  };

  Utils._convertData = function (data) {
    for (var originalKey in data) {
      var keys = originalKey.split('-');

      var dataLevel = data;

      if (keys.length === 1) {
        continue;
      }

      for (var k = 0; k < keys.length; k++) {
        var key = keys[k];

        // Lowercase the first letter
        // By default, dash-separated becomes camelCase
        key = key.substring(0, 1).toLowerCase() + key.substring(1);

        if (!(key in dataLevel)) {
          dataLevel[key] = {};
        }

        if (k == keys.length - 1) {
          dataLevel[key] = data[originalKey];
        }

        dataLevel = dataLevel[key];
      }

      delete data[originalKey];
    }

    return data;
  };

  Utils.hasScroll = function (index, el) {
    // Adapted from the function created by @ShadowScripter
    // and adapted by @BillBarry on the Stack Exchange Code Review website.
    // The original code can be found at
    // http://codereview.stackexchange.com/q/13338
    // and was designed to be used with the Sizzle selector engine.

    var $el = $(el);
    var overflowX = el.style.overflowX;
    var overflowY = el.style.overflowY;

    //Check both x and y declarations
    if (overflowX === overflowY &&
        (overflowY === 'hidden' || overflowY === 'visible')) {
      return false;
    }

    if (overflowX === 'scroll' || overflowY === 'scroll') {
      return true;
    }

    return ($el.innerHeight() < el.scrollHeight ||
      $el.innerWidth() < el.scrollWidth);
  };

  Utils.escapeMarkup = function (markup) {
    var replaceMap = {
      '\\\\': '&#92;',
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      '\\'': '&#39;',
      '/': '&#47;'
    };

    // Do not try to escape the markup if it's not a string
    if (typeof markup !== 'string') {
      return markup;
    }

    return String(markup).replace(/[&<>"'\\/\\\\]/g, function (match) {
      return replaceMap[match];
    });
  };

  // Cache objects in Utils.__cache instead of $.data (see #4346)
  Utils.__cache = {};

  var id = 0;
  Utils.GetUniqueElementId = function (element) {
    // Get a unique element Id. If element has no id,
    // creates a new unique number, stores it in the id
    // attribute and returns the new id with a prefix.
    // If an id already exists, it simply returns it with a prefix.

    var select2Id = element.getAttribute('data-select2-id');

    if (select2Id != null) {
      return select2Id;
    }

    // If element has id, use it.
    if (element.id) {
      select2Id = 'select2-data-' + element.id;
    } else {
      select2Id = 'select2-data-' + (++id).toString() +
        '-' + Utils.generateChars(4);
    }

    element.setAttribute('data-select2-id', select2Id);

    return select2Id;
  };

  Utils.StoreData = function (element, name, value) {
    // Stores an item in the cache for a specified element.
    // name is the cache key.
    var id = Utils.GetUniqueElementId(element);
    if (!Utils.__cache[id]) {
      Utils.__cache[id] = {};
    }

    Utils.__cache[id][name] = value;
  };

  Utils.GetData = function (element, name) {
    // Retrieves a value from the cache by its key (name)
    // name is optional. If no name specified, return
    // all cache items for the specified element.
    // and for a specified element.
    var id = Utils.GetUniqueElementId(element);
    if (name) {
      if (Utils.__cache[id]) {
        if (Utils.__cache[id][name] != null) {
          return Utils.__cache[id][name];
        }
        return $(element).data(name); // Fallback to HTML5 data attribs.
      }
      return $(element).data(name); // Fallback to HTML5 data attribs.
    } else {
      return Utils.__cache[id];
    }
  };

  Utils.RemoveData = function (element) {
    // Removes all cached items for a specified element.
    var id = Utils.GetUniqueElementId(element);
    if (Utils.__cache[id] != null) {
      delete Utils.__cache[id];
    }

    element.removeAttribute('data-select2-id');
  };

  Utils.copyNonInternalCssClasses = function (dest, src) {
    var classes;

    var destinationClasses = dest.getAttribute('class').trim().split(/\\s+/);

    destinationClasses = destinationClasses.filter(function (clazz) {
      // Save all Select2 classes
      return clazz.indexOf('select2-') === 0;
    });

    var sourceClasses = src.getAttribute('class').trim().split(/\\s+/);

    sourceClasses = sourceClasses.filter(function (clazz) {
      // Only copy non-Select2 classes
      return clazz.indexOf('select2-') !== 0;
    });

    var replacements = destinationClasses.concat(sourceClasses);

    dest.setAttribute('class', replacements.join(' '));
  };

  return Utils;
});

S2.define('select2/results',[
  'jquery',
  './utils'
], function ($, Utils) {
  function Results ($element, options, dataAdapter) {
    this.$element = $element;
    this.data = dataAdapter;
    this.options = options;

    Results.__super__.constructor.call(this);
  }

  Utils.Extend(Results, Utils.Observable);

  Results.prototype.render = function () {
    var $results = $(
      '<ul class="select2-results__options" role="listbox"></ul>'
    );

    if (this.options.get('multiple')) {
      $results.attr('aria-multiselectable', 'true');
    }

    this.$results = $results;

    return $results;
  };

  Results.prototype.clear = function () {
    this.$results.empty();
  };

  Results.prototype.displayMessage = function (params) {
    var escapeMarkup = this.options.get('escapeMarkup');

    this.clear();
    this.hideLoading();

    var $message = $(
      '<li role="alert" aria-live="assertive"' +
      ' class="select2-results__option"></li>'
    );

    var message = this.options.get('translations').get(params.message);

    $message.append(
      escapeMarkup(
        message(params.args)
      )
    );

    $message[0].className += ' select2-results__message';

    this.$results.append($message);
  };

  Results.prototype.hideMessages = function () {
    this.$results.find('.select2-results__message').remove();
  };

  Results.prototype.append = function (data) {
    this.hideLoading();

    var $options = [];

    if (data.results == null || data.results.length === 0) {
      if (this.$results.children().length === 0) {
        this.trigger('results:message', {
          message: 'noResults'
        });
      }

      return;
    }

    data.results = this.sort(data.results);

    for (var d = 0; d < data.results.length; d++) {
      var item = data.results[d];

      var $option = this.option(item);

      $options.push($option);
    }

    this.$results.append($options);
  };

  Results.prototype.position = function ($results, $dropdown) {
    var $resultsContainer = $dropdown.find('.select2-results');
    $resultsContainer.append($results);
  };

  Results.prototype.sort = function (data) {
    var sorter = this.options.get('sorter');

    return sorter(data);
  };

  Results.prototype.highlightFirstItem = function () {
    var $options = this.$results
      .find('.select2-results__option--selectable');

    var $selected = $options.filter('.select2-results__option--selected');

    // Check if there are any selected options
    if ($selected.length > 0) {
      // If there are selected options, highlight the first
      $selected.first().trigger('mouseenter');
    } else {
      // If there are no selected options, highlight the first option
      // in the dropdown
      $options.first().trigger('mouseenter');
    }

    this.ensureHighlightVisible();
  };

  Results.prototype.setClasses = function () {
    var self = this;

    this.data.current(function (selected) {
      var selectedIds = selected.map(function (s) {
        return s.id.toString();
      });

      var $options = self.$results
        .find('.select2-results__option--selectable');

      $options.each(function () {
        var $option = $(this);

        var item = Utils.GetData(this, 'data');

        // id needs to be converted to a string when comparing
        var id = '' + item.id;

        if ((item.element != null && item.element.selected) ||
            (item.element == null && selectedIds.indexOf(id) > -1)) {
          this.classList.add('select2-results__option--selected');
          $option.attr('aria-selected', 'true');
        } else {
          this.classList.remove('select2-results__option--selected');
          $option.attr('aria-selected', 'false');
        }
      });

    });
  };

  Results.prototype.showLoading = function (params) {
    this.hideLoading();

    var loadingMore = this.options.get('translations').get('searching');

    var loading = {
      disabled: true,
      loading: true,
      text: loadingMore(params)
    };
    var $loading = this.option(loading);
    $loading.className += ' loading-results';

    this.$results.prepend($loading);
  };

  Results.prototype.hideLoading = function () {
    this.$results.find('.loading-results').remove();
  };

  Results.prototype.option = function (data) {
    var option = document.createElement('li');
    option.classList.add('select2-results__option');
    option.classList.add('select2-results__option--selectable');

    var attrs = {
      'role': 'option'
    };

    var matches = window.Element.prototype.matches ||
      window.Element.prototype.msMatchesSelector ||
      window.Element.prototype.webkitMatchesSelector;

    if ((data.element != null && matches.call(data.element, ':disabled')) ||
        (data.element == null && data.disabled)) {
      attrs['aria-disabled'] = 'true';

      option.classList.remove('select2-results__option--selectable');
      option.classList.add('select2-results__option--disabled');
    }

    if (data.id == null) {
      option.classList.remove('select2-results__option--selectable');
    }

    if (data._resultId != null) {
      option.id = data._resultId;
    }

    if (data.title) {
      option.title = data.title;
    }

    if (data.children) {
      attrs.role = 'group';
      attrs['aria-label'] = data.text;

      option.classList.remove('select2-results__option--selectable');
      option.classList.add('select2-results__option--group');
    }

    for (var attr in attrs) {
      var val = attrs[attr];

      option.setAttribute(attr, val);
    }

    if (data.children) {
      var $option = $(option);

      var label = document.createElement('strong');
      label.className = 'select2-results__group';

      this.template(data, label);

      var $children = [];

      for (var c = 0; c < data.children.length; c++) {
        var child = data.children[c];

        var $child = this.option(child);

        $children.push($child);
      }

      var $childrenContainer = $('<ul></ul>', {
        'class': 'select2-results__options select2-results__options--nested',
        'role': 'none'
      });

      $childrenContainer.append($children);

      $option.append(label);
      $option.append($childrenContainer);
    } else {
      this.template(data, option);
    }

    Utils.StoreData(option, 'data', data);

    return option;
  };

  Results.prototype.bind = function (container, $container) {
    var self = this;

    var id = container.id + '-results';

    this.$results.attr('id', id);

    container.on('results:all', function (params) {
      self.clear();
      self.append(params.data);

      if (container.isOpen()) {
        self.setClasses();
        self.highlightFirstItem();
      }
    });

    container.on('results:append', function (params) {
      self.append(params.data);

      if (container.isOpen()) {
        self.setClasses();
      }
    });

    container.on('query', function (params) {
      self.hideMessages();
      self.showLoading(params);
    });

    container.on('select', function () {
      if (!container.isOpen()) {
        return;
      }

      self.setClasses();

      if (self.options.get('scrollAfterSelect')) {
        self.highlightFirstItem();
      }
    });

    container.on('unselect', function () {
      if (!container.isOpen()) {
        return;
      }

      self.setClasses();

      if (self.options.get('scrollAfterSelect')) {
        self.highlightFirstItem();
      }
    });

    container.on('open', function () {
      // When the dropdown is open, aria-expended="true"
      self.$results.attr('aria-expanded', 'true');
      self.$results.attr('aria-hidden', 'false');

      self.setClasses();
      self.ensureHighlightVisible();
    });

    container.on('close', function () {
      // When the dropdown is closed, aria-expended="false"
      self.$results.attr('aria-expanded', 'false');
      self.$results.attr('aria-hidden', 'true');
      self.$results.removeAttr('aria-activedescendant');
    });

    container.on('results:toggle', function () {
      var $highlighted = self.getHighlightedResults();

      if ($highlighted.length === 0) {
        return;
      }

      $highlighted.trigger('mouseup');
    });

    container.on('results:select', function () {
      var $highlighted = self.getHighlightedResults();

      if ($highlighted.length === 0) {
        return;
      }

      var data = Utils.GetData($highlighted[0], 'data');

      if ($highlighted.hasClass('select2-results__option--selected')) {
        self.trigger('close', {});
      } else {
        self.trigger('select', {
          data: data
        });
      }
    });

    container.on('results:previous', function () {
      var $highlighted = self.getHighlightedResults();

      var $options = self.$results.find('.select2-results__option--selectable');

      var currentIndex = $options.index($highlighted);

      // If we are already at the top, don't move further
      // If no options, currentIndex will be -1
      if (currentIndex <= 0) {
        return;
      }

      var nextIndex = currentIndex - 1;

      // If none are highlighted, highlight the first
      if ($highlighted.length === 0) {
        nextIndex = 0;
      }

      var $next = $options.eq(nextIndex);

      $next.trigger('mouseenter');

      var currentOffset = self.$results.offset().top;
      var nextTop = $next.offset().top;
      var nextOffset = self.$results.scrollTop() + (nextTop - currentOffset);

      if (nextIndex === 0) {
        self.$results.scrollTop(0);
      } else if (nextTop - currentOffset < 0) {
        self.$results.scrollTop(nextOffset);
      }
    });

    container.on('results:next', function () {
      var $highlighted = self.getHighlightedResults();

      var $options = self.$results.find('.select2-results__option--selectable');

      var currentIndex = $options.index($highlighted);

      var nextIndex = currentIndex + 1;

      // If we are at the last option, stay there
      if (nextIndex >= $options.length) {
        return;
      }

      var $next = $options.eq(nextIndex);

      $next.trigger('mouseenter');

      var currentOffset = self.$results.offset().top +
        self.$results.outerHeight(false);
      var nextBottom = $next.offset().top + $next.outerHeight(false);
      var nextOffset = self.$results.scrollTop() + nextBottom - currentOffset;

      if (nextIndex === 0) {
        self.$results.scrollTop(0);
      } else if (nextBottom > currentOffset) {
        self.$results.scrollTop(nextOffset);
      }
    });

    container.on('results:focus', function (params) {
      params.element[0].classList.add('select2-results__option--highlighted');
      params.element[0].setAttribute('aria-selected', 'true');
    });

    container.on('results:message', function (params) {
      self.displayMessage(params);
    });

    if ($.fn.mousewheel) {
      this.$results.on('mousewheel', function (e) {
        var top = self.$results.scrollTop();

        var bottom = self.$results.get(0).scrollHeight - top + e.deltaY;

        var isAtTop = e.deltaY > 0 && top - e.deltaY <= 0;
        var isAtBottom = e.deltaY < 0 && bottom <= self.$results.height();

        if (isAtTop) {
          self.$results.scrollTop(0);

          e.preventDefault();
          e.stopPropagation();
        } else if (isAtBottom) {
          self.$results.scrollTop(
            self.$results.get(0).scrollHeight - self.$results.height()
          );

          e.preventDefault();
          e.stopPropagation();
        }
      });
    }

    this.$results.on('mouseup', '.select2-results__option--selectable',
      function (evt) {
      var $this = $(this);

      var data = Utils.GetData(this, 'data');

      if ($this.hasClass('select2-results__option--selected')) {
        if (self.options.get('multiple')) {
          self.trigger('unselect', {
            originalEvent: evt,
            data: data
          });
        } else {
          self.trigger('close', {});
        }

        return;
      }

      self.trigger('select', {
        originalEvent: evt,
        data: data
      });
    });

    this.$results.on('mouseenter', '.select2-results__option--selectable',
      function (evt) {
      var data = Utils.GetData(this, 'data');

      self.getHighlightedResults()
          .removeClass('select2-results__option--highlighted')
          .attr('aria-selected', 'false');

      self.trigger('results:focus', {
        data: data,
        element: $(this)
      });
    });
  };

  Results.prototype.getHighlightedResults = function () {
    var $highlighted = this.$results
    .find('.select2-results__option--highlighted');

    return $highlighted;
  };

  Results.prototype.destroy = function () {
    this.$results.remove();
  };

  Results.prototype.ensureHighlightVisible = function () {
    var $highlighted = this.getHighlightedResults();

    if ($highlighted.length === 0) {
      return;
    }

    var $options = this.$results.find('.select2-results__option--selectable');

    var currentIndex = $options.index($highlighted);

    var currentOffset = this.$results.offset().top;
    var nextTop = $highlighted.offset().top;
    var nextOffset = this.$results.scrollTop() + (nextTop - currentOffset);

    var offsetDelta = nextTop - currentOffset;
    nextOffset -= $highlighted.outerHeight(false) * 2;

    if (currentIndex <= 2) {
      this.$results.scrollTop(0);
    } else if (offsetDelta > this.$results.outerHeight() || offsetDelta < 0) {
      this.$results.scrollTop(nextOffset);
    }
  };

  Results.prototype.template = function (result, container) {
    var template = this.options.get('templateResult');
    var escapeMarkup = this.options.get('escapeMarkup');

    var content = template(result, container);

    if (content == null) {
      container.style.display = 'none';
    } else if (typeof content === 'string') {
      container.innerHTML = escapeMarkup(content);
    } else {
      $(container).append(content);
    }
  };

  return Results;
});

S2.define('select2/keys',[

], function () {
  var KEYS = {
    BACKSPACE: 8,
    TAB: 9,
    ENTER: 13,
    SHIFT: 16,
    CTRL: 17,
    ALT: 18,
    ESC: 27,
    SPACE: 32,
    PAGE_UP: 33,
    PAGE_DOWN: 34,
    END: 35,
    HOME: 36,
    LEFT: 37,
    UP: 38,
    RIGHT: 39,
    DOWN: 40,
    DELETE: 46
  };

  return KEYS;
});

S2.define('select2/selection/base',[
  'jquery',
  '../utils',
  '../keys'
], function ($, Utils, KEYS) {
  function BaseSelection ($element, options) {
    this.$element = $element;
    this.options = options;

    BaseSelection.__super__.constructor.call(this);
  }

  Utils.Extend(BaseSelection, Utils.Observable);

  BaseSelection.prototype.render = function () {
    var $selection = $(
      '<span class="select2-selection" role="combobox" ' +
      ' aria-haspopup="true" aria-expanded="false">' +
      '</span>'
    );

    this._tabindex = 0;

    if (Utils.GetData(this.$element[0], 'old-tabindex') != null) {
      this._tabindex = Utils.GetData(this.$element[0], 'old-tabindex');
    } else if (this.$element.attr('tabindex') != null) {
      this._tabindex = this.$element.attr('tabindex');
    }

    $selection.attr('title', this.$element.attr('title'));
    $selection.attr('tabindex', this._tabindex);
    $selection.attr('aria-disabled', 'false');

    this.$selection = $selection;

    return $selection;
  };

  BaseSelection.prototype.bind = function (container, $container) {
    var self = this;

    var resultsId = container.id + '-results';

    this.container = container;

    this.$selection.on('focus', function (evt) {
      self.trigger('focus', evt);
    });

    this.$selection.on('blur', function (evt) {
      self._handleBlur(evt);
    });

    this.$selection.on('keydown', function (evt) {
      self.trigger('keypress', evt);

      if (evt.which === KEYS.SPACE) {
        evt.preventDefault();
      }
    });

    container.on('results:focus', function (params) {
      self.$selection.attr('aria-activedescendant', params.data._resultId);
    });

    container.on('selection:update', function (params) {
      self.update(params.data);
    });

    container.on('open', function () {
      // When the dropdown is open, aria-expanded="true"
      self.$selection.attr('aria-expanded', 'true');
      self.$selection.attr('aria-owns', resultsId);

      self._attachCloseHandler(container);
    });

    container.on('close', function () {
      // When the dropdown is closed, aria-expanded="false"
      self.$selection.attr('aria-expanded', 'false');
      self.$selection.removeAttr('aria-activedescendant');
      self.$selection.removeAttr('aria-owns');

      self.$selection.trigger('focus');

      self._detachCloseHandler(container);
    });

    container.on('enable', function () {
      self.$selection.attr('tabindex', self._tabindex);
      self.$selection.attr('aria-disabled', 'false');
    });

    container.on('disable', function () {
      self.$selection.attr('tabindex', '-1');
      self.$selection.attr('aria-disabled', 'true');
    });
  };

  BaseSelection.prototype._handleBlur = function (evt) {
    var self = this;

    // This needs to be delayed as the active element is the body when the tab
    // key is pressed, possibly along with others.
    window.setTimeout(function () {
      // Don't trigger \`blur\` if the focus is still in the selection
      if (
        (document.activeElement == self.$selection[0]) ||
        ($.contains(self.$selection[0], document.activeElement))
      ) {
        return;
      }

      self.trigger('blur', evt);
    }, 1);
  };

  BaseSelection.prototype._attachCloseHandler = function (container) {

    $(document.body).on('mousedown.select2.' + container.id, function (e) {
      var $target = $(e.target);

      var $select = $target.closest('.select2');

      var $all = $('.select2.select2-container--open');

      $all.each(function () {
        if (this == $select[0]) {
          return;
        }

        var $element = Utils.GetData(this, 'element');

        $element.select2('close');
      });
    });
  };

  BaseSelection.prototype._detachCloseHandler = function (container) {
    $(document.body).off('mousedown.select2.' + container.id);
  };

  BaseSelection.prototype.position = function ($selection, $container) {
    var $selectionContainer = $container.find('.selection');
    $selectionContainer.append($selection);
  };

  BaseSelection.prototype.destroy = function () {
    this._detachCloseHandler(this.container);
  };

  BaseSelection.prototype.update = function (data) {
    throw new Error('The \`update\` method must be defined in child classes.');
  };

  /**
   * Helper method to abstract the "enabled" (not "disabled") state of this
   * object.
   *
   * @return {true} if the instance is not disabled.
   * @return {false} if the instance is disabled.
   */
  BaseSelection.prototype.isEnabled = function () {
    return !this.isDisabled();
  };

  /**
   * Helper method to abstract the "disabled" state of this object.
   *
   * @return {true} if the disabled option is true.
   * @return {false} if the disabled option is false.
   */
  BaseSelection.prototype.isDisabled = function () {
    return this.options.get('disabled');
  };

  return BaseSelection;
});

S2.define('select2/selection/single',[
  'jquery',
  './base',
  '../utils',
  '../keys'
], function ($, BaseSelection, Utils, KEYS) {
  function SingleSelection () {
    SingleSelection.__super__.constructor.apply(this, arguments);
  }

  Utils.Extend(SingleSelection, BaseSelection);

  SingleSelection.prototype.render = function () {
    var $selection = SingleSelection.__super__.render.call(this);

    $selection[0].classList.add('select2-selection--single');

    $selection.html(
      '<span class="select2-selection__rendered"></span>' +
      '<span class="select2-selection__arrow" role="presentation">' +
        '<b role="presentation"></b>' +
      '</span>'
    );

    return $selection;
  };

  SingleSelection.prototype.bind = function (container, $container) {
    var self = this;

    SingleSelection.__super__.bind.apply(this, arguments);

    var id = container.id + '-container';

    this.$selection.find('.select2-selection__rendered')
      .attr('id', id)
      .attr('role', 'textbox')
      .attr('aria-readonly', 'true');
    this.$selection.attr('aria-labelledby', id);
    this.$selection.attr('aria-controls', id);

    this.$selection.on('mousedown', function (evt) {
      // Only respond to left clicks
      if (evt.which !== 1) {
        return;
      }

      self.trigger('toggle', {
        originalEvent: evt
      });
    });

    this.$selection.on('focus', function (evt) {
      // User focuses on the container
    });

    this.$selection.on('blur', function (evt) {
      // User exits the container
    });

    container.on('focus', function (evt) {
      if (!container.isOpen()) {
        self.$selection.trigger('focus');
      }
    });
  };

  SingleSelection.prototype.clear = function () {
    var $rendered = this.$selection.find('.select2-selection__rendered');
    $rendered.empty();
    $rendered.removeAttr('title'); // clear tooltip on empty
  };

  SingleSelection.prototype.display = function (data, container) {
    var template = this.options.get('templateSelection');
    var escapeMarkup = this.options.get('escapeMarkup');

    return escapeMarkup(template(data, container));
  };

  SingleSelection.prototype.selectionContainer = function () {
    return $('<span></span>');
  };

  SingleSelection.prototype.update = function (data) {
    if (data.length === 0) {
      this.clear();
      return;
    }

    var selection = data[0];

    var $rendered = this.$selection.find('.select2-selection__rendered');
    var formatted = this.display(selection, $rendered);

    $rendered.empty().append(formatted);

    var title = selection.title || selection.text;

    if (title) {
      $rendered.attr('title', title);
    } else {
      $rendered.removeAttr('title');
    }
  };

  return SingleSelection;
});

S2.define('select2/selection/multiple',[
  'jquery',
  './base',
  '../utils'
], function ($, BaseSelection, Utils) {
  function MultipleSelection ($element, options) {
    MultipleSelection.__super__.constructor.apply(this, arguments);
  }

  Utils.Extend(MultipleSelection, BaseSelection);

  MultipleSelection.prototype.render = function () {
    var $selection = MultipleSelection.__super__.render.call(this);

    $selection[0].classList.add('select2-selection--multiple');

    $selection.html(
      '<ul class="select2-selection__rendered"></ul>'
    );

    return $selection;
  };

  MultipleSelection.prototype.bind = function (container, $container) {
    var self = this;

    MultipleSelection.__super__.bind.apply(this, arguments);

    var id = container.id + '-container';
    this.$selection.find('.select2-selection__rendered').attr('id', id);

    this.$selection.on('click', function (evt) {
      self.trigger('toggle', {
        originalEvent: evt
      });
    });

    this.$selection.on(
      'click',
      '.select2-selection__choice__remove',
      function (evt) {
        // Ignore the event if it is disabled
        if (self.isDisabled()) {
          return;
        }

        var $remove = $(this);
        var $selection = $remove.parent();

        var data = Utils.GetData($selection[0], 'data');

        self.trigger('unselect', {
          originalEvent: evt,
          data: data
        });
      }
    );

    this.$selection.on(
      'keydown',
      '.select2-selection__choice__remove',
      function (evt) {
        // Ignore the event if it is disabled
        if (self.isDisabled()) {
          return;
        }

        evt.stopPropagation();
      }
    );
  };

  MultipleSelection.prototype.clear = function () {
    var $rendered = this.$selection.find('.select2-selection__rendered');
    $rendered.empty();
    $rendered.removeAttr('title');
  };

  MultipleSelection.prototype.display = function (data, container) {
    var template = this.options.get('templateSelection');
    var escapeMarkup = this.options.get('escapeMarkup');

    return escapeMarkup(template(data, container));
  };

  MultipleSelection.prototype.selectionContainer = function () {
    var $container = $(
      '<li class="select2-selection__choice">' +
        '<button type="button" class="select2-selection__choice__remove" ' +
        'tabindex="-1">' +
          '<span aria-hidden="true">&times;</span>' +
        '</button>' +
        '<span class="select2-selection__choice__display"></span>' +
      '</li>'
    );

    return $container;
  };

  MultipleSelection.prototype.update = function (data) {
    this.clear();

    if (data.length === 0) {
      return;
    }

    var $selections = [];

    var selectionIdPrefix = this.$selection.find('.select2-selection__rendered')
      .attr('id') + '-choice-';

    for (var d = 0; d < data.length; d++) {
      var selection = data[d];

      var $selection = this.selectionContainer();
      var formatted = this.display(selection, $selection);

      var selectionId = selectionIdPrefix + Utils.generateChars(4) + '-';

      if (selection.id) {
        selectionId += selection.id;
      } else {
        selectionId += Utils.generateChars(4);
      }

      $selection.find('.select2-selection__choice__display')
        .append(formatted)
        .attr('id', selectionId);

      var title = selection.title || selection.text;

      if (title) {
        $selection.attr('title', title);
      }

      var removeItem = this.options.get('translations').get('removeItem');

      var $remove = $selection.find('.select2-selection__choice__remove');

      $remove.attr('title', removeItem());
      $remove.attr('aria-label', removeItem());
      $remove.attr('aria-describedby', selectionId);

      Utils.StoreData($selection[0], 'data', selection);

      $selections.push($selection);
    }

    var $rendered = this.$selection.find('.select2-selection__rendered');

    $rendered.append($selections);
  };

  return MultipleSelection;
});

S2.define('select2/selection/placeholder',[

], function () {
  function Placeholder (decorated, $element, options) {
    this.placeholder = this.normalizePlaceholder(options.get('placeholder'));

    decorated.call(this, $element, options);
  }

  Placeholder.prototype.normalizePlaceholder = function (_, placeholder) {
    if (typeof placeholder === 'string') {
      placeholder = {
        id: '',
        text: placeholder
      };
    }

    return placeholder;
  };

  Placeholder.prototype.createPlaceholder = function (decorated, placeholder) {
    var $placeholder = this.selectionContainer();

    $placeholder.html(this.display(placeholder));
    $placeholder[0].classList.add('select2-selection__placeholder');
    $placeholder[0].classList.remove('select2-selection__choice');

    var placeholderTitle = placeholder.title ||
      placeholder.text ||
      $placeholder.text();

    this.$selection.find('.select2-selection__rendered').attr(
      'title',
      placeholderTitle
    );

    return $placeholder;
  };

  Placeholder.prototype.update = function (decorated, data) {
    var singlePlaceholder = (
      data.length == 1 && data[0].id != this.placeholder.id
    );
    var multipleSelections = data.length > 1;

    if (multipleSelections || singlePlaceholder) {
      return decorated.call(this, data);
    }

    this.clear();

    var $placeholder = this.createPlaceholder(this.placeholder);

    this.$selection.find('.select2-selection__rendered').append($placeholder);
  };

  return Placeholder;
});

S2.define('select2/selection/allowClear',[
  'jquery',
  '../keys',
  '../utils'
], function ($, KEYS, Utils) {
  function AllowClear () { }

  AllowClear.prototype.bind = function (decorated, container, $container) {
    var self = this;

    decorated.call(this, container, $container);

    if (this.placeholder == null) {
      if (this.options.get('debug') && window.console && console.error) {
        console.error(
          'Select2: The \`allowClear\` option should be used in combination ' +
          'with the \`placeholder\` option.'
        );
      }
    }

    this.$selection.on('mousedown', '.select2-selection__clear',
      function (evt) {
        self._handleClear(evt);
    });

    container.on('keypress', function (evt) {
      self._handleKeyboardClear(evt, container);
    });
  };

  AllowClear.prototype._handleClear = function (_, evt) {
    // Ignore the event if it is disabled
    if (this.isDisabled()) {
      return;
    }

    var $clear = this.$selection.find('.select2-selection__clear');

    // Ignore the event if nothing has been selected
    if ($clear.length === 0) {
      return;
    }

    evt.stopPropagation();

    var data = Utils.GetData($clear[0], 'data');

    var previousVal = this.$element.val();
    this.$element.val(this.placeholder.id);

    var unselectData = {
      data: data
    };
    this.trigger('clear', unselectData);
    if (unselectData.prevented) {
      this.$element.val(previousVal);
      return;
    }

    for (var d = 0; d < data.length; d++) {
      unselectData = {
        data: data[d]
      };

      // Trigger the \`unselect\` event, so people can prevent it from being
      // cleared.
      this.trigger('unselect', unselectData);

      // If the event was prevented, don't clear it out.
      if (unselectData.prevented) {
        this.$element.val(previousVal);
        return;
      }
    }

    this.$element.trigger('input').trigger('change');

    this.trigger('toggle', {});
  };

  AllowClear.prototype._handleKeyboardClear = function (_, evt, container) {
    if (container.isOpen()) {
      return;
    }

    if (evt.which == KEYS.DELETE || evt.which == KEYS.BACKSPACE) {
      this._handleClear(evt);
    }
  };

  AllowClear.prototype.update = function (decorated, data) {
    decorated.call(this, data);

    this.$selection.find('.select2-selection__clear').remove();
    this.$selection[0].classList.remove('select2-selection--clearable');

    if (this.$selection.find('.select2-selection__placeholder').length > 0 ||
        data.length === 0) {
      return;
    }

    var selectionId = this.$selection.find('.select2-selection__rendered')
      .attr('id');

    var removeAll = this.options.get('translations').get('removeAllItems');

    var $remove = $(
      '<button type="button" class="select2-selection__clear" tabindex="-1">' +
        '<span aria-hidden="true">&times;</span>' +
      '</button>'
    );
    $remove.attr('title', removeAll());
    $remove.attr('aria-label', removeAll());
    $remove.attr('aria-describedby', selectionId);
    Utils.StoreData($remove[0], 'data', data);

    this.$selection.prepend($remove);
    this.$selection[0].classList.add('select2-selection--clearable');
  };

  return AllowClear;
});

S2.define('select2/selection/search',[
  'jquery',
  '../utils',
  '../keys'
], function ($, Utils, KEYS) {
  function Search (decorated, $element, options) {
    decorated.call(this, $element, options);
  }

  Search.prototype.render = function (decorated) {
    var searchLabel = this.options.get('translations').get('search');
    var $search = $(
      '<span class="select2-search select2-search--inline">' +
        '<textarea class="select2-search__field"'+
        ' type="search" tabindex="-1"' +
        ' autocorrect="off" autocapitalize="none"' +
        ' spellcheck="false" role="searchbox" aria-autocomplete="list" >' +
        '</textarea>' +
      '</span>'
    );

    this.$searchContainer = $search;
    this.$search = $search.find('textarea');

    this.$search.prop('autocomplete', this.options.get('autocomplete'));
    this.$search.attr('aria-label', searchLabel());

    var $rendered = decorated.call(this);

    this._transferTabIndex();
    $rendered.append(this.$searchContainer);

    return $rendered;
  };

  Search.prototype.bind = function (decorated, container, $container) {
    var self = this;

    var resultsId = container.id + '-results';
    var selectionId = container.id + '-container';

    decorated.call(this, container, $container);

    self.$search.attr('aria-describedby', selectionId);

    container.on('open', function () {
      self.$search.attr('aria-controls', resultsId);
      self.$search.trigger('focus');
    });

    container.on('close', function () {
      self.$search.val('');
      self.resizeSearch();
      self.$search.removeAttr('aria-controls');
      self.$search.removeAttr('aria-activedescendant');
      self.$search.trigger('focus');
    });

    container.on('enable', function () {
      self.$search.prop('disabled', false);

      self._transferTabIndex();
    });

    container.on('disable', function () {
      self.$search.prop('disabled', true);
    });

    container.on('focus', function (evt) {
      self.$search.trigger('focus');
    });

    container.on('results:focus', function (params) {
      if (params.data._resultId) {
        self.$search.attr('aria-activedescendant', params.data._resultId);
      } else {
        self.$search.removeAttr('aria-activedescendant');
      }
    });

    this.$selection.on('focusin', '.select2-search--inline', function (evt) {
      self.trigger('focus', evt);
    });

    this.$selection.on('focusout', '.select2-search--inline', function (evt) {
      self._handleBlur(evt);
    });

    this.$selection.on('keydown', '.select2-search--inline', function (evt) {
      evt.stopPropagation();

      self.trigger('keypress', evt);

      self._keyUpPrevented = evt.isDefaultPrevented();

      var key = evt.which;

      if (key === KEYS.BACKSPACE && self.$search.val() === '') {
        var $previousChoice = self.$selection
          .find('.select2-selection__choice').last();

        if ($previousChoice.length > 0) {
          var item = Utils.GetData($previousChoice[0], 'data');

          self.searchRemoveChoice(item);

          evt.preventDefault();
        }
      }
    });

    this.$selection.on('click', '.select2-search--inline', function (evt) {
      if (self.$search.val()) {
        evt.stopPropagation();
      }
    });

    // Try to detect the IE version should the \`documentMode\` property that
    // is stored on the document. This is only implemented in IE and is
    // slightly cleaner than doing a user agent check.
    // This property is not available in Edge, but Edge also doesn't have
    // this bug.
    var msie = document.documentMode;
    var disableInputEvents = msie && msie <= 11;

    // Workaround for browsers which do not support the \`input\` event
    // This will prevent double-triggering of events for browsers which support
    // both the \`keyup\` and \`input\` events.
    this.$selection.on(
      'input.searchcheck',
      '.select2-search--inline',
      function (evt) {
        // IE will trigger the \`input\` event when a placeholder is used on a
        // search box. To get around this issue, we are forced to ignore all
        // \`input\` events in IE and keep using \`keyup\`.
        if (disableInputEvents) {
          self.$selection.off('input.search input.searchcheck');
          return;
        }

        // Unbind the duplicated \`keyup\` event
        self.$selection.off('keyup.search');
      }
    );

    this.$selection.on(
      'keyup.search input.search',
      '.select2-search--inline',
      function (evt) {
        // IE will trigger the \`input\` event when a placeholder is used on a
        // search box. To get around this issue, we are forced to ignore all
        // \`input\` events in IE and keep using \`keyup\`.
        if (disableInputEvents && evt.type === 'input') {
          self.$selection.off('input.search input.searchcheck');
          return;
        }

        var key = evt.which;

        // We can freely ignore events from modifier keys
        if (key == KEYS.SHIFT || key == KEYS.CTRL || key == KEYS.ALT) {
          return;
        }

        // Tabbing will be handled during the \`keydown\` phase
        if (key == KEYS.TAB) {
          return;
        }

        self.handleSearch(evt);
      }
    );
  };

  /**
   * This method will transfer the tabindex attribute from the rendered
   * selection to the search box. This allows for the search box to be used as
   * the primary focus instead of the selection container.
   *
   * @private
   */
  Search.prototype._transferTabIndex = function (decorated) {
    this.$search.attr('tabindex', this.$selection.attr('tabindex'));
    this.$selection.attr('tabindex', '-1');
  };

  Search.prototype.createPlaceholder = function (decorated, placeholder) {
    this.$search.attr('placeholder', placeholder.text);
  };

  Search.prototype.update = function (decorated, data) {
    var searchHadFocus = this.$search[0] == document.activeElement;

    this.$search.attr('placeholder', '');

    decorated.call(this, data);

    this.resizeSearch();
    if (searchHadFocus) {
      this.$search.trigger('focus');
    }
  };

  Search.prototype.handleSearch = function () {
    this.resizeSearch();

    if (!this._keyUpPrevented) {
      var input = this.$search.val();

      this.trigger('query', {
        term: input
      });
    }

    this._keyUpPrevented = false;
  };

  Search.prototype.searchRemoveChoice = function (decorated, item) {
    this.trigger('unselect', {
      data: item
    });

    this.$search.val(item.text);
    this.handleSearch();
  };

  Search.prototype.resizeSearch = function () {
    this.$search.css('width', '25px');

    var width = '100%';

    if (this.$search.attr('placeholder') === '') {
      var minimumWidth = this.$search.val().length + 1;

      width = (minimumWidth * 0.75) + 'em';
    }

    this.$search.css('width', width);
  };

  return Search;
});

S2.define('select2/selection/selectionCss',[
  '../utils'
], function (Utils) {
  function SelectionCSS () { }

  SelectionCSS.prototype.render = function (decorated) {
    var $selection = decorated.call(this);

    var selectionCssClass = this.options.get('selectionCssClass') || '';

    if (selectionCssClass.indexOf(':all:') !== -1) {
      selectionCssClass = selectionCssClass.replace(':all:', '');

      Utils.copyNonInternalCssClasses($selection[0], this.$element[0]);
    }

    $selection.addClass(selectionCssClass);

    return $selection;
  };

  return SelectionCSS;
});

S2.define('select2/selection/eventRelay',[
  'jquery'
], function ($) {
  function EventRelay () { }

  EventRelay.prototype.bind = function (decorated, container, $container) {
    var self = this;
    var relayEvents = [
      'open', 'opening',
      'close', 'closing',
      'select', 'selecting',
      'unselect', 'unselecting',
      'clear', 'clearing'
    ];

    var preventableEvents = [
      'opening', 'closing', 'selecting', 'unselecting', 'clearing'
    ];

    decorated.call(this, container, $container);

    container.on('*', function (name, params) {
      // Ignore events that should not be relayed
      if (relayEvents.indexOf(name) === -1) {
        return;
      }

      // The parameters should always be an object
      params = params || {};

      // Generate the jQuery event for the Select2 event
      var evt = $.Event('select2:' + name, {
        params: params
      });

      self.$element.trigger(evt);

      // Only handle preventable events if it was one
      if (preventableEvents.indexOf(name) === -1) {
        return;
      }

      params.prevented = evt.isDefaultPrevented();
    });
  };

  return EventRelay;
});

S2.define('select2/translation',[
  'jquery',
  'require'
], function ($, require) {
  function Translation (dict) {
    this.dict = dict || {};
  }

  Translation.prototype.all = function () {
    return this.dict;
  };

  Translation.prototype.get = function (key) {
    return this.dict[key];
  };

  Translation.prototype.extend = function (translation) {
    this.dict = $.extend({}, translation.all(), this.dict);
  };

  // Static functions

  Translation._cache = {};

  Translation.loadPath = function (path) {
    if (!(path in Translation._cache)) {
      var translations = require(path);

      Translation._cache[path] = translations;
    }

    return new Translation(Translation._cache[path]);
  };

  return Translation;
});

S2.define('select2/diacritics',[

], function () {
  var diacritics = {
    '\\u24B6': 'A',
    '\\uFF21': 'A',
    '\\u00C0': 'A',
    '\\u00C1': 'A',
    '\\u00C2': 'A',
    '\\u1EA6': 'A',
    '\\u1EA4': 'A',
    '\\u1EAA': 'A',
    '\\u1EA8': 'A',
    '\\u00C3': 'A',
    '\\u0100': 'A',
    '\\u0102': 'A',
    '\\u1EB0': 'A',
    '\\u1EAE': 'A',
    '\\u1EB4': 'A',
    '\\u1EB2': 'A',
    '\\u0226': 'A',
    '\\u01E0': 'A',
    '\\u00C4': 'A',
    '\\u01DE': 'A',
    '\\u1EA2': 'A',
    '\\u00C5': 'A',
    '\\u01FA': 'A',
    '\\u01CD': 'A',
    '\\u0200': 'A',
    '\\u0202': 'A',
    '\\u1EA0': 'A',
    '\\u1EAC': 'A',
    '\\u1EB6': 'A',
    '\\u1E00': 'A',
    '\\u0104': 'A',
    '\\u023A': 'A',
    '\\u2C6F': 'A',
    '\\uA732': 'AA',
    '\\u00C6': 'AE',
    '\\u01FC': 'AE',
    '\\u01E2': 'AE',
    '\\uA734': 'AO',
    '\\uA736': 'AU',
    '\\uA738': 'AV',
    '\\uA73A': 'AV',
    '\\uA73C': 'AY',
    '\\u24B7': 'B',
    '\\uFF22': 'B',
    '\\u1E02': 'B',
    '\\u1E04': 'B',
    '\\u1E06': 'B',
    '\\u0243': 'B',
    '\\u0182': 'B',
    '\\u0181': 'B',
    '\\u24B8': 'C',
    '\\uFF23': 'C',
    '\\u0106': 'C',
    '\\u0108': 'C',
    '\\u010A': 'C',
    '\\u010C': 'C',
    '\\u00C7': 'C',
    '\\u1E08': 'C',
    '\\u0187': 'C',
    '\\u023B': 'C',
    '\\uA73E': 'C',
    '\\u24B9': 'D',
    '\\uFF24': 'D',
    '\\u1E0A': 'D',
    '\\u010E': 'D',
    '\\u1E0C': 'D',
    '\\u1E10': 'D',
    '\\u1E12': 'D',
    '\\u1E0E': 'D',
    '\\u0110': 'D',
    '\\u018B': 'D',
    '\\u018A': 'D',
    '\\u0189': 'D',
    '\\uA779': 'D',
    '\\u01F1': 'DZ',
    '\\u01C4': 'DZ',
    '\\u01F2': 'Dz',
    '\\u01C5': 'Dz',
    '\\u24BA': 'E',
    '\\uFF25': 'E',
    '\\u00C8': 'E',
    '\\u00C9': 'E',
    '\\u00CA': 'E',
    '\\u1EC0': 'E',
    '\\u1EBE': 'E',
    '\\u1EC4': 'E',
    '\\u1EC2': 'E',
    '\\u1EBC': 'E',
    '\\u0112': 'E',
    '\\u1E14': 'E',
    '\\u1E16': 'E',
    '\\u0114': 'E',
    '\\u0116': 'E',
    '\\u00CB': 'E',
    '\\u1EBA': 'E',
    '\\u011A': 'E',
    '\\u0204': 'E',
    '\\u0206': 'E',
    '\\u1EB8': 'E',
    '\\u1EC6': 'E',
    '\\u0228': 'E',
    '\\u1E1C': 'E',
    '\\u0118': 'E',
    '\\u1E18': 'E',
    '\\u1E1A': 'E',
    '\\u0190': 'E',
    '\\u018E': 'E',
    '\\u24BB': 'F',
    '\\uFF26': 'F',
    '\\u1E1E': 'F',
    '\\u0191': 'F',
    '\\uA77B': 'F',
    '\\u24BC': 'G',
    '\\uFF27': 'G',
    '\\u01F4': 'G',
    '\\u011C': 'G',
    '\\u1E20': 'G',
    '\\u011E': 'G',
    '\\u0120': 'G',
    '\\u01E6': 'G',
    '\\u0122': 'G',
    '\\u01E4': 'G',
    '\\u0193': 'G',
    '\\uA7A0': 'G',
    '\\uA77D': 'G',
    '\\uA77E': 'G',
    '\\u24BD': 'H',
    '\\uFF28': 'H',
    '\\u0124': 'H',
    '\\u1E22': 'H',
    '\\u1E26': 'H',
    '\\u021E': 'H',
    '\\u1E24': 'H',
    '\\u1E28': 'H',
    '\\u1E2A': 'H',
    '\\u0126': 'H',
    '\\u2C67': 'H',
    '\\u2C75': 'H',
    '\\uA78D': 'H',
    '\\u24BE': 'I',
    '\\uFF29': 'I',
    '\\u00CC': 'I',
    '\\u00CD': 'I',
    '\\u00CE': 'I',
    '\\u0128': 'I',
    '\\u012A': 'I',
    '\\u012C': 'I',
    '\\u0130': 'I',
    '\\u00CF': 'I',
    '\\u1E2E': 'I',
    '\\u1EC8': 'I',
    '\\u01CF': 'I',
    '\\u0208': 'I',
    '\\u020A': 'I',
    '\\u1ECA': 'I',
    '\\u012E': 'I',
    '\\u1E2C': 'I',
    '\\u0197': 'I',
    '\\u24BF': 'J',
    '\\uFF2A': 'J',
    '\\u0134': 'J',
    '\\u0248': 'J',
    '\\u24C0': 'K',
    '\\uFF2B': 'K',
    '\\u1E30': 'K',
    '\\u01E8': 'K',
    '\\u1E32': 'K',
    '\\u0136': 'K',
    '\\u1E34': 'K',
    '\\u0198': 'K',
    '\\u2C69': 'K',
    '\\uA740': 'K',
    '\\uA742': 'K',
    '\\uA744': 'K',
    '\\uA7A2': 'K',
    '\\u24C1': 'L',
    '\\uFF2C': 'L',
    '\\u013F': 'L',
    '\\u0139': 'L',
    '\\u013D': 'L',
    '\\u1E36': 'L',
    '\\u1E38': 'L',
    '\\u013B': 'L',
    '\\u1E3C': 'L',
    '\\u1E3A': 'L',
    '\\u0141': 'L',
    '\\u023D': 'L',
    '\\u2C62': 'L',
    '\\u2C60': 'L',
    '\\uA748': 'L',
    '\\uA746': 'L',
    '\\uA780': 'L',
    '\\u01C7': 'LJ',
    '\\u01C8': 'Lj',
    '\\u24C2': 'M',
    '\\uFF2D': 'M',
    '\\u1E3E': 'M',
    '\\u1E40': 'M',
    '\\u1E42': 'M',
    '\\u2C6E': 'M',
    '\\u019C': 'M',
    '\\u24C3': 'N',
    '\\uFF2E': 'N',
    '\\u01F8': 'N',
    '\\u0143': 'N',
    '\\u00D1': 'N',
    '\\u1E44': 'N',
    '\\u0147': 'N',
    '\\u1E46': 'N',
    '\\u0145': 'N',
    '\\u1E4A': 'N',
    '\\u1E48': 'N',
    '\\u0220': 'N',
    '\\u019D': 'N',
    '\\uA790': 'N',
    '\\uA7A4': 'N',
    '\\u01CA': 'NJ',
    '\\u01CB': 'Nj',
    '\\u24C4': 'O',
    '\\uFF2F': 'O',
    '\\u00D2': 'O',
    '\\u00D3': 'O',
    '\\u00D4': 'O',
    '\\u1ED2': 'O',
    '\\u1ED0': 'O',
    '\\u1ED6': 'O',
    '\\u1ED4': 'O',
    '\\u00D5': 'O',
    '\\u1E4C': 'O',
    '\\u022C': 'O',
    '\\u1E4E': 'O',
    '\\u014C': 'O',
    '\\u1E50': 'O',
    '\\u1E52': 'O',
    '\\u014E': 'O',
    '\\u022E': 'O',
    '\\u0230': 'O',
    '\\u00D6': 'O',
    '\\u022A': 'O',
    '\\u1ECE': 'O',
    '\\u0150': 'O',
    '\\u01D1': 'O',
    '\\u020C': 'O',
    '\\u020E': 'O',
    '\\u01A0': 'O',
    '\\u1EDC': 'O',
    '\\u1EDA': 'O',
    '\\u1EE0': 'O',
    '\\u1EDE': 'O',
    '\\u1EE2': 'O',
    '\\u1ECC': 'O',
    '\\u1ED8': 'O',
    '\\u01EA': 'O',
    '\\u01EC': 'O',
    '\\u00D8': 'O',
    '\\u01FE': 'O',
    '\\u0186': 'O',
    '\\u019F': 'O',
    '\\uA74A': 'O',
    '\\uA74C': 'O',
    '\\u0152': 'OE',
    '\\u01A2': 'OI',
    '\\uA74E': 'OO',
    '\\u0222': 'OU',
    '\\u24C5': 'P',
    '\\uFF30': 'P',
    '\\u1E54': 'P',
    '\\u1E56': 'P',
    '\\u01A4': 'P',
    '\\u2C63': 'P',
    '\\uA750': 'P',
    '\\uA752': 'P',
    '\\uA754': 'P',
    '\\u24C6': 'Q',
    '\\uFF31': 'Q',
    '\\uA756': 'Q',
    '\\uA758': 'Q',
    '\\u024A': 'Q',
    '\\u24C7': 'R',
    '\\uFF32': 'R',
    '\\u0154': 'R',
    '\\u1E58': 'R',
    '\\u0158': 'R',
    '\\u0210': 'R',
    '\\u0212': 'R',
    '\\u1E5A': 'R',
    '\\u1E5C': 'R',
    '\\u0156': 'R',
    '\\u1E5E': 'R',
    '\\u024C': 'R',
    '\\u2C64': 'R',
    '\\uA75A': 'R',
    '\\uA7A6': 'R',
    '\\uA782': 'R',
    '\\u24C8': 'S',
    '\\uFF33': 'S',
    '\\u1E9E': 'S',
    '\\u015A': 'S',
    '\\u1E64': 'S',
    '\\u015C': 'S',
    '\\u1E60': 'S',
    '\\u0160': 'S',
    '\\u1E66': 'S',
    '\\u1E62': 'S',
    '\\u1E68': 'S',
    '\\u0218': 'S',
    '\\u015E': 'S',
    '\\u2C7E': 'S',
    '\\uA7A8': 'S',
    '\\uA784': 'S',
    '\\u24C9': 'T',
    '\\uFF34': 'T',
    '\\u1E6A': 'T',
    '\\u0164': 'T',
    '\\u1E6C': 'T',
    '\\u021A': 'T',
    '\\u0162': 'T',
    '\\u1E70': 'T',
    '\\u1E6E': 'T',
    '\\u0166': 'T',
    '\\u01AC': 'T',
    '\\u01AE': 'T',
    '\\u023E': 'T',
    '\\uA786': 'T',
    '\\uA728': 'TZ',
    '\\u24CA': 'U',
    '\\uFF35': 'U',
    '\\u00D9': 'U',
    '\\u00DA': 'U',
    '\\u00DB': 'U',
    '\\u0168': 'U',
    '\\u1E78': 'U',
    '\\u016A': 'U',
    '\\u1E7A': 'U',
    '\\u016C': 'U',
    '\\u00DC': 'U',
    '\\u01DB': 'U',
    '\\u01D7': 'U',
    '\\u01D5': 'U',
    '\\u01D9': 'U',
    '\\u1EE6': 'U',
    '\\u016E': 'U',
    '\\u0170': 'U',
    '\\u01D3': 'U',
    '\\u0214': 'U',
    '\\u0216': 'U',
    '\\u01AF': 'U',
    '\\u1EEA': 'U',
    '\\u1EE8': 'U',
    '\\u1EEE': 'U',
    '\\u1EEC': 'U',
    '\\u1EF0': 'U',
    '\\u1EE4': 'U',
    '\\u1E72': 'U',
    '\\u0172': 'U',
    '\\u1E76': 'U',
    '\\u1E74': 'U',
    '\\u0244': 'U',
    '\\u24CB': 'V',
    '\\uFF36': 'V',
    '\\u1E7C': 'V',
    '\\u1E7E': 'V',
    '\\u01B2': 'V',
    '\\uA75E': 'V',
    '\\u0245': 'V',
    '\\uA760': 'VY',
    '\\u24CC': 'W',
    '\\uFF37': 'W',
    '\\u1E80': 'W',
    '\\u1E82': 'W',
    '\\u0174': 'W',
    '\\u1E86': 'W',
    '\\u1E84': 'W',
    '\\u1E88': 'W',
    '\\u2C72': 'W',
    '\\u24CD': 'X',
    '\\uFF38': 'X',
    '\\u1E8A': 'X',
    '\\u1E8C': 'X',
    '\\u24CE': 'Y',
    '\\uFF39': 'Y',
    '\\u1EF2': 'Y',
    '\\u00DD': 'Y',
    '\\u0176': 'Y',
    '\\u1EF8': 'Y',
    '\\u0232': 'Y',
    '\\u1E8E': 'Y',
    '\\u0178': 'Y',
    '\\u1EF6': 'Y',
    '\\u1EF4': 'Y',
    '\\u01B3': 'Y',
    '\\u024E': 'Y',
    '\\u1EFE': 'Y',
    '\\u24CF': 'Z',
    '\\uFF3A': 'Z',
    '\\u0179': 'Z',
    '\\u1E90': 'Z',
    '\\u017B': 'Z',
    '\\u017D': 'Z',
    '\\u1E92': 'Z',
    '\\u1E94': 'Z',
    '\\u01B5': 'Z',
    '\\u0224': 'Z',
    '\\u2C7F': 'Z',
    '\\u2C6B': 'Z',
    '\\uA762': 'Z',
    '\\u24D0': 'a',
    '\\uFF41': 'a',
    '\\u1E9A': 'a',
    '\\u00E0': 'a',
    '\\u00E1': 'a',
    '\\u00E2': 'a',
    '\\u1EA7': 'a',
    '\\u1EA5': 'a',
    '\\u1EAB': 'a',
    '\\u1EA9': 'a',
    '\\u00E3': 'a',
    '\\u0101': 'a',
    '\\u0103': 'a',
    '\\u1EB1': 'a',
    '\\u1EAF': 'a',
    '\\u1EB5': 'a',
    '\\u1EB3': 'a',
    '\\u0227': 'a',
    '\\u01E1': 'a',
    '\\u00E4': 'a',
    '\\u01DF': 'a',
    '\\u1EA3': 'a',
    '\\u00E5': 'a',
    '\\u01FB': 'a',
    '\\u01CE': 'a',
    '\\u0201': 'a',
    '\\u0203': 'a',
    '\\u1EA1': 'a',
    '\\u1EAD': 'a',
    '\\u1EB7': 'a',
    '\\u1E01': 'a',
    '\\u0105': 'a',
    '\\u2C65': 'a',
    '\\u0250': 'a',
    '\\uA733': 'aa',
    '\\u00E6': 'ae',
    '\\u01FD': 'ae',
    '\\u01E3': 'ae',
    '\\uA735': 'ao',
    '\\uA737': 'au',
    '\\uA739': 'av',
    '\\uA73B': 'av',
    '\\uA73D': 'ay',
    '\\u24D1': 'b',
    '\\uFF42': 'b',
    '\\u1E03': 'b',
    '\\u1E05': 'b',
    '\\u1E07': 'b',
    '\\u0180': 'b',
    '\\u0183': 'b',
    '\\u0253': 'b',
    '\\u24D2': 'c',
    '\\uFF43': 'c',
    '\\u0107': 'c',
    '\\u0109': 'c',
    '\\u010B': 'c',
    '\\u010D': 'c',
    '\\u00E7': 'c',
    '\\u1E09': 'c',
    '\\u0188': 'c',
    '\\u023C': 'c',
    '\\uA73F': 'c',
    '\\u2184': 'c',
    '\\u24D3': 'd',
    '\\uFF44': 'd',
    '\\u1E0B': 'd',
    '\\u010F': 'd',
    '\\u1E0D': 'd',
    '\\u1E11': 'd',
    '\\u1E13': 'd',
    '\\u1E0F': 'd',
    '\\u0111': 'd',
    '\\u018C': 'd',
    '\\u0256': 'd',
    '\\u0257': 'd',
    '\\uA77A': 'd',
    '\\u01F3': 'dz',
    '\\u01C6': 'dz',
    '\\u24D4': 'e',
    '\\uFF45': 'e',
    '\\u00E8': 'e',
    '\\u00E9': 'e',
    '\\u00EA': 'e',
    '\\u1EC1': 'e',
    '\\u1EBF': 'e',
    '\\u1EC5': 'e',
    '\\u1EC3': 'e',
    '\\u1EBD': 'e',
    '\\u0113': 'e',
    '\\u1E15': 'e',
    '\\u1E17': 'e',
    '\\u0115': 'e',
    '\\u0117': 'e',
    '\\u00EB': 'e',
    '\\u1EBB': 'e',
    '\\u011B': 'e',
    '\\u0205': 'e',
    '\\u0207': 'e',
    '\\u1EB9': 'e',
    '\\u1EC7': 'e',
    '\\u0229': 'e',
    '\\u1E1D': 'e',
    '\\u0119': 'e',
    '\\u1E19': 'e',
    '\\u1E1B': 'e',
    '\\u0247': 'e',
    '\\u025B': 'e',
    '\\u01DD': 'e',
    '\\u24D5': 'f',
    '\\uFF46': 'f',
    '\\u1E1F': 'f',
    '\\u0192': 'f',
    '\\uA77C': 'f',
    '\\u24D6': 'g',
    '\\uFF47': 'g',
    '\\u01F5': 'g',
    '\\u011D': 'g',
    '\\u1E21': 'g',
    '\\u011F': 'g',
    '\\u0121': 'g',
    '\\u01E7': 'g',
    '\\u0123': 'g',
    '\\u01E5': 'g',
    '\\u0260': 'g',
    '\\uA7A1': 'g',
    '\\u1D79': 'g',
    '\\uA77F': 'g',
    '\\u24D7': 'h',
    '\\uFF48': 'h',
    '\\u0125': 'h',
    '\\u1E23': 'h',
    '\\u1E27': 'h',
    '\\u021F': 'h',
    '\\u1E25': 'h',
    '\\u1E29': 'h',
    '\\u1E2B': 'h',
    '\\u1E96': 'h',
    '\\u0127': 'h',
    '\\u2C68': 'h',
    '\\u2C76': 'h',
    '\\u0265': 'h',
    '\\u0195': 'hv',
    '\\u24D8': 'i',
    '\\uFF49': 'i',
    '\\u00EC': 'i',
    '\\u00ED': 'i',
    '\\u00EE': 'i',
    '\\u0129': 'i',
    '\\u012B': 'i',
    '\\u012D': 'i',
    '\\u00EF': 'i',
    '\\u1E2F': 'i',
    '\\u1EC9': 'i',
    '\\u01D0': 'i',
    '\\u0209': 'i',
    '\\u020B': 'i',
    '\\u1ECB': 'i',
    '\\u012F': 'i',
    '\\u1E2D': 'i',
    '\\u0268': 'i',
    '\\u0131': 'i',
    '\\u24D9': 'j',
    '\\uFF4A': 'j',
    '\\u0135': 'j',
    '\\u01F0': 'j',
    '\\u0249': 'j',
    '\\u24DA': 'k',
    '\\uFF4B': 'k',
    '\\u1E31': 'k',
    '\\u01E9': 'k',
    '\\u1E33': 'k',
    '\\u0137': 'k',
    '\\u1E35': 'k',
    '\\u0199': 'k',
    '\\u2C6A': 'k',
    '\\uA741': 'k',
    '\\uA743': 'k',
    '\\uA745': 'k',
    '\\uA7A3': 'k',
    '\\u24DB': 'l',
    '\\uFF4C': 'l',
    '\\u0140': 'l',
    '\\u013A': 'l',
    '\\u013E': 'l',
    '\\u1E37': 'l',
    '\\u1E39': 'l',
    '\\u013C': 'l',
    '\\u1E3D': 'l',
    '\\u1E3B': 'l',
    '\\u017F': 'l',
    '\\u0142': 'l',
    '\\u019A': 'l',
    '\\u026B': 'l',
    '\\u2C61': 'l',
    '\\uA749': 'l',
    '\\uA781': 'l',
    '\\uA747': 'l',
    '\\u01C9': 'lj',
    '\\u24DC': 'm',
    '\\uFF4D': 'm',
    '\\u1E3F': 'm',
    '\\u1E41': 'm',
    '\\u1E43': 'm',
    '\\u0271': 'm',
    '\\u026F': 'm',
    '\\u24DD': 'n',
    '\\uFF4E': 'n',
    '\\u01F9': 'n',
    '\\u0144': 'n',
    '\\u00F1': 'n',
    '\\u1E45': 'n',
    '\\u0148': 'n',
    '\\u1E47': 'n',
    '\\u0146': 'n',
    '\\u1E4B': 'n',
    '\\u1E49': 'n',
    '\\u019E': 'n',
    '\\u0272': 'n',
    '\\u0149': 'n',
    '\\uA791': 'n',
    '\\uA7A5': 'n',
    '\\u01CC': 'nj',
    '\\u24DE': 'o',
    '\\uFF4F': 'o',
    '\\u00F2': 'o',
    '\\u00F3': 'o',
    '\\u00F4': 'o',
    '\\u1ED3': 'o',
    '\\u1ED1': 'o',
    '\\u1ED7': 'o',
    '\\u1ED5': 'o',
    '\\u00F5': 'o',
    '\\u1E4D': 'o',
    '\\u022D': 'o',
    '\\u1E4F': 'o',
    '\\u014D': 'o',
    '\\u1E51': 'o',
    '\\u1E53': 'o',
    '\\u014F': 'o',
    '\\u022F': 'o',
    '\\u0231': 'o',
    '\\u00F6': 'o',
    '\\u022B': 'o',
    '\\u1ECF': 'o',
    '\\u0151': 'o',
    '\\u01D2': 'o',
    '\\u020D': 'o',
    '\\u020F': 'o',
    '\\u01A1': 'o',
    '\\u1EDD': 'o',
    '\\u1EDB': 'o',
    '\\u1EE1': 'o',
    '\\u1EDF': 'o',
    '\\u1EE3': 'o',
    '\\u1ECD': 'o',
    '\\u1ED9': 'o',
    '\\u01EB': 'o',
    '\\u01ED': 'o',
    '\\u00F8': 'o',
    '\\u01FF': 'o',
    '\\u0254': 'o',
    '\\uA74B': 'o',
    '\\uA74D': 'o',
    '\\u0275': 'o',
    '\\u0153': 'oe',
    '\\u01A3': 'oi',
    '\\u0223': 'ou',
    '\\uA74F': 'oo',
    '\\u24DF': 'p',
    '\\uFF50': 'p',
    '\\u1E55': 'p',
    '\\u1E57': 'p',
    '\\u01A5': 'p',
    '\\u1D7D': 'p',
    '\\uA751': 'p',
    '\\uA753': 'p',
    '\\uA755': 'p',
    '\\u24E0': 'q',
    '\\uFF51': 'q',
    '\\u024B': 'q',
    '\\uA757': 'q',
    '\\uA759': 'q',
    '\\u24E1': 'r',
    '\\uFF52': 'r',
    '\\u0155': 'r',
    '\\u1E59': 'r',
    '\\u0159': 'r',
    '\\u0211': 'r',
    '\\u0213': 'r',
    '\\u1E5B': 'r',
    '\\u1E5D': 'r',
    '\\u0157': 'r',
    '\\u1E5F': 'r',
    '\\u024D': 'r',
    '\\u027D': 'r',
    '\\uA75B': 'r',
    '\\uA7A7': 'r',
    '\\uA783': 'r',
    '\\u24E2': 's',
    '\\uFF53': 's',
    '\\u00DF': 's',
    '\\u015B': 's',
    '\\u1E65': 's',
    '\\u015D': 's',
    '\\u1E61': 's',
    '\\u0161': 's',
    '\\u1E67': 's',
    '\\u1E63': 's',
    '\\u1E69': 's',
    '\\u0219': 's',
    '\\u015F': 's',
    '\\u023F': 's',
    '\\uA7A9': 's',
    '\\uA785': 's',
    '\\u1E9B': 's',
    '\\u24E3': 't',
    '\\uFF54': 't',
    '\\u1E6B': 't',
    '\\u1E97': 't',
    '\\u0165': 't',
    '\\u1E6D': 't',
    '\\u021B': 't',
    '\\u0163': 't',
    '\\u1E71': 't',
    '\\u1E6F': 't',
    '\\u0167': 't',
    '\\u01AD': 't',
    '\\u0288': 't',
    '\\u2C66': 't',
    '\\uA787': 't',
    '\\uA729': 'tz',
    '\\u24E4': 'u',
    '\\uFF55': 'u',
    '\\u00F9': 'u',
    '\\u00FA': 'u',
    '\\u00FB': 'u',
    '\\u0169': 'u',
    '\\u1E79': 'u',
    '\\u016B': 'u',
    '\\u1E7B': 'u',
    '\\u016D': 'u',
    '\\u00FC': 'u',
    '\\u01DC': 'u',
    '\\u01D8': 'u',
    '\\u01D6': 'u',
    '\\u01DA': 'u',
    '\\u1EE7': 'u',
    '\\u016F': 'u',
    '\\u0171': 'u',
    '\\u01D4': 'u',
    '\\u0215': 'u',
    '\\u0217': 'u',
    '\\u01B0': 'u',
    '\\u1EEB': 'u',
    '\\u1EE9': 'u',
    '\\u1EEF': 'u',
    '\\u1EED': 'u',
    '\\u1EF1': 'u',
    '\\u1EE5': 'u',
    '\\u1E73': 'u',
    '\\u0173': 'u',
    '\\u1E77': 'u',
    '\\u1E75': 'u',
    '\\u0289': 'u',
    '\\u24E5': 'v',
    '\\uFF56': 'v',
    '\\u1E7D': 'v',
    '\\u1E7F': 'v',
    '\\u028B': 'v',
    '\\uA75F': 'v',
    '\\u028C': 'v',
    '\\uA761': 'vy',
    '\\u24E6': 'w',
    '\\uFF57': 'w',
    '\\u1E81': 'w',
    '\\u1E83': 'w',
    '\\u0175': 'w',
    '\\u1E87': 'w',
    '\\u1E85': 'w',
    '\\u1E98': 'w',
    '\\u1E89': 'w',
    '\\u2C73': 'w',
    '\\u24E7': 'x',
    '\\uFF58': 'x',
    '\\u1E8B': 'x',
    '\\u1E8D': 'x',
    '\\u24E8': 'y',
    '\\uFF59': 'y',
    '\\u1EF3': 'y',
    '\\u00FD': 'y',
    '\\u0177': 'y',
    '\\u1EF9': 'y',
    '\\u0233': 'y',
    '\\u1E8F': 'y',
    '\\u00FF': 'y',
    '\\u1EF7': 'y',
    '\\u1E99': 'y',
    '\\u1EF5': 'y',
    '\\u01B4': 'y',
    '\\u024F': 'y',
    '\\u1EFF': 'y',
    '\\u24E9': 'z',
    '\\uFF5A': 'z',
    '\\u017A': 'z',
    '\\u1E91': 'z',
    '\\u017C': 'z',
    '\\u017E': 'z',
    '\\u1E93': 'z',
    '\\u1E95': 'z',
    '\\u01B6': 'z',
    '\\u0225': 'z',
    '\\u0240': 'z',
    '\\u2C6C': 'z',
    '\\uA763': 'z',
    '\\u0386': '\\u0391',
    '\\u0388': '\\u0395',
    '\\u0389': '\\u0397',
    '\\u038A': '\\u0399',
    '\\u03AA': '\\u0399',
    '\\u038C': '\\u039F',
    '\\u038E': '\\u03A5',
    '\\u03AB': '\\u03A5',
    '\\u038F': '\\u03A9',
    '\\u03AC': '\\u03B1',
    '\\u03AD': '\\u03B5',
    '\\u03AE': '\\u03B7',
    '\\u03AF': '\\u03B9',
    '\\u03CA': '\\u03B9',
    '\\u0390': '\\u03B9',
    '\\u03CC': '\\u03BF',
    '\\u03CD': '\\u03C5',
    '\\u03CB': '\\u03C5',
    '\\u03B0': '\\u03C5',
    '\\u03CE': '\\u03C9',
    '\\u03C2': '\\u03C3',
    '\\u2019': '\\''
  };

  return diacritics;
});

S2.define('select2/data/base',[
  '../utils'
], function (Utils) {
  function BaseAdapter ($element, options) {
    BaseAdapter.__super__.constructor.call(this);
  }

  Utils.Extend(BaseAdapter, Utils.Observable);

  BaseAdapter.prototype.current = function (callback) {
    throw new Error('The \`current\` method must be defined in child classes.');
  };

  BaseAdapter.prototype.query = function (params, callback) {
    throw new Error('The \`query\` method must be defined in child classes.');
  };

  BaseAdapter.prototype.bind = function (container, $container) {
    // Can be implemented in subclasses
  };

  BaseAdapter.prototype.destroy = function () {
    // Can be implemented in subclasses
  };

  BaseAdapter.prototype.generateResultId = function (container, data) {
    var id = container.id + '-result-';

    id += Utils.generateChars(4);

    if (data.id != null) {
      id += '-' + data.id.toString();
    } else {
      id += '-' + Utils.generateChars(4);
    }
    return id;
  };

  return BaseAdapter;
});

S2.define('select2/data/select',[
  './base',
  '../utils',
  'jquery'
], function (BaseAdapter, Utils, $) {
  function SelectAdapter ($element, options) {
    this.$element = $element;
    this.options = options;

    SelectAdapter.__super__.constructor.call(this);
  }

  Utils.Extend(SelectAdapter, BaseAdapter);

  SelectAdapter.prototype.current = function (callback) {
    var self = this;

    var data = Array.prototype.map.call(
      this.$element[0].querySelectorAll(':checked'),
      function (selectedElement) {
        return self.item($(selectedElement));
      }
    );

    callback(data);
  };

  SelectAdapter.prototype.select = function (data) {
    var self = this;

    data.selected = true;

    // If data.element is a DOM node, use it instead
    if (
      data.element != null && data.element.tagName.toLowerCase() === 'option'
    ) {
      data.element.selected = true;

      this.$element.trigger('input').trigger('change');

      return;
    }

    if (this.$element.prop('multiple')) {
      this.current(function (currentData) {
        var val = [];

        data = [data];
        data.push.apply(data, currentData);

        for (var d = 0; d < data.length; d++) {
          var id = data[d].id;

          if (val.indexOf(id) === -1) {
            val.push(id);
          }
        }

        self.$element.val(val);
        self.$element.trigger('input').trigger('change');
      });
    } else {
      var val = data.id;

      this.$element.val(val);
      this.$element.trigger('input').trigger('change');
    }
  };

  SelectAdapter.prototype.unselect = function (data) {
    var self = this;

    if (!this.$element.prop('multiple')) {
      return;
    }

    data.selected = false;

    if (
      data.element != null &&
      data.element.tagName.toLowerCase() === 'option'
    ) {
      data.element.selected = false;

      this.$element.trigger('input').trigger('change');

      return;
    }

    this.current(function (currentData) {
      var val = [];

      for (var d = 0; d < currentData.length; d++) {
        var id = currentData[d].id;

        if (id !== data.id && val.indexOf(id) === -1) {
          val.push(id);
        }
      }

      self.$element.val(val);

      self.$element.trigger('input').trigger('change');
    });
  };

  SelectAdapter.prototype.bind = function (container, $container) {
    var self = this;

    this.container = container;

    container.on('select', function (params) {
      self.select(params.data);
    });

    container.on('unselect', function (params) {
      self.unselect(params.data);
    });
  };

  SelectAdapter.prototype.destroy = function () {
    // Remove anything added to child elements
    this.$element.find('*').each(function () {
      // Remove any custom data set by Select2
      Utils.RemoveData(this);
    });
  };

  SelectAdapter.prototype.query = function (params, callback) {
    var data = [];
    var self = this;

    var $options = this.$element.children();

    $options.each(function () {
      if (
        this.tagName.toLowerCase() !== 'option' &&
        this.tagName.toLowerCase() !== 'optgroup'
      ) {
        return;
      }

      var $option = $(this);

      var option = self.item($option);

      var matches = self.matches(params, option);

      if (matches !== null) {
        data.push(matches);
      }
    });

    callback({
      results: data
    });
  };

  SelectAdapter.prototype.addOptions = function ($options) {
    this.$element.append($options);
  };

  SelectAdapter.prototype.option = function (data) {
    var option;

    if (data.children) {
      option = document.createElement('optgroup');
      option.label = data.text;
    } else {
      option = document.createElement('option');

      if (option.textContent !== undefined) {
        option.textContent = data.text;
      } else {
        option.innerText = data.text;
      }
    }

    if (data.id !== undefined) {
      option.value = data.id;
    }

    if (data.disabled) {
      option.disabled = true;
    }

    if (data.selected) {
      option.selected = true;
    }

    if (data.title) {
      option.title = data.title;
    }

    var normalizedData = this._normalizeItem(data);
    normalizedData.element = option;

    // Override the option's data with the combined data
    Utils.StoreData(option, 'data', normalizedData);

    return $(option);
  };

  SelectAdapter.prototype.item = function ($option) {
    var data = {};

    data = Utils.GetData($option[0], 'data');

    if (data != null) {
      return data;
    }

    var option = $option[0];

    if (option.tagName.toLowerCase() === 'option') {
      data = {
        id: $option.val(),
        text: $option.text(),
        disabled: $option.prop('disabled'),
        selected: $option.prop('selected'),
        title: $option.prop('title')
      };
    } else if (option.tagName.toLowerCase() === 'optgroup') {
      data = {
        text: $option.prop('label'),
        children: [],
        title: $option.prop('title')
      };

      var $children = $option.children('option');
      var children = [];

      for (var c = 0; c < $children.length; c++) {
        var $child = $($children[c]);

        var child = this.item($child);

        children.push(child);
      }

      data.children = children;
    }

    data = this._normalizeItem(data);
    data.element = $option[0];

    Utils.StoreData($option[0], 'data', data);

    return data;
  };

  SelectAdapter.prototype._normalizeItem = function (item) {
    if (item !== Object(item)) {
      item = {
        id: item,
        text: item
      };
    }

    item = $.extend({}, {
      text: ''
    }, item);

    var defaults = {
      selected: false,
      disabled: false
    };

    if (item.id != null) {
      item.id = item.id.toString();
    }

    if (item.text != null) {
      item.text = item.text.toString();
    }

    if (item._resultId == null && item.id && this.container != null) {
      item._resultId = this.generateResultId(this.container, item);
    }

    return $.extend({}, defaults, item);
  };

  SelectAdapter.prototype.matches = function (params, data) {
    var matcher = this.options.get('matcher');

    return matcher(params, data);
  };

  return SelectAdapter;
});

S2.define('select2/data/array',[
  './select',
  '../utils',
  'jquery'
], function (SelectAdapter, Utils, $) {
  function ArrayAdapter ($element, options) {
    this._dataToConvert = options.get('data') || [];

    ArrayAdapter.__super__.constructor.call(this, $element, options);
  }

  Utils.Extend(ArrayAdapter, SelectAdapter);

  ArrayAdapter.prototype.bind = function (container, $container) {
    ArrayAdapter.__super__.bind.call(this, container, $container);

    this.addOptions(this.convertToOptions(this._dataToConvert));
  };

  ArrayAdapter.prototype.select = function (data) {
    var $option = this.$element.find('option').filter(function (i, elm) {
      return elm.value == data.id.toString();
    });

    if ($option.length === 0) {
      $option = this.option(data);

      this.addOptions($option);
    }

    ArrayAdapter.__super__.select.call(this, data);
  };

  ArrayAdapter.prototype.convertToOptions = function (data) {
    var self = this;

    var $existing = this.$element.find('option');
    var existingIds = $existing.map(function () {
      return self.item($(this)).id;
    }).get();

    var $options = [];

    // Filter out all items except for the one passed in the argument
    function onlyItem (item) {
      return function () {
        return $(this).val() == item.id;
      };
    }

    for (var d = 0; d < data.length; d++) {
      var item = this._normalizeItem(data[d]);

      // Skip items which were pre-loaded, only merge the data
      if (existingIds.indexOf(item.id) >= 0) {
        var $existingOption = $existing.filter(onlyItem(item));

        var existingData = this.item($existingOption);
        var newData = $.extend(true, {}, item, existingData);

        var $newOption = this.option(newData);

        $existingOption.replaceWith($newOption);

        continue;
      }

      var $option = this.option(item);

      if (item.children) {
        var $children = this.convertToOptions(item.children);

        $option.append($children);
      }

      $options.push($option);
    }

    return $options;
  };

  return ArrayAdapter;
});

S2.define('select2/data/ajax',[
  './array',
  '../utils',
  'jquery'
], function (ArrayAdapter, Utils, $) {
  function AjaxAdapter ($element, options) {
    this.ajaxOptions = this._applyDefaults(options.get('ajax'));

    if (this.ajaxOptions.processResults != null) {
      this.processResults = this.ajaxOptions.processResults;
    }

    AjaxAdapter.__super__.constructor.call(this, $element, options);
  }

  Utils.Extend(AjaxAdapter, ArrayAdapter);

  AjaxAdapter.prototype._applyDefaults = function (options) {
    var defaults = {
      data: function (params) {
        return $.extend({}, params, {
          q: params.term
        });
      },
      transport: function (params, success, failure) {
        var $request = $.ajax(params);

        $request.then(success);
        $request.fail(failure);

        return $request;
      }
    };

    return $.extend({}, defaults, options, true);
  };

  AjaxAdapter.prototype.processResults = function (results) {
    return results;
  };

  AjaxAdapter.prototype.query = function (params, callback) {
    var matches = [];
    var self = this;

    if (this._request != null) {
      // JSONP requests cannot always be aborted
      if (typeof this._request.abort === 'function') {
        this._request.abort();
      }

      this._request = null;
    }

    var options = $.extend({
      type: 'GET'
    }, this.ajaxOptions);

    if (typeof options.url === 'function') {
      options.url = options.url.call(this.$element, params);
    }

    if (typeof options.data === 'function') {
      options.data = options.data.call(this.$element, params);
    }

    function request () {
      var $request = options.transport(options, function (data) {
        var results = self.processResults(data, params);

        if (self.options.get('debug') && window.console && console.error) {
          // Check to make sure that the response included a \`results\` key.
          if (!results || !results.results || !Array.isArray(results.results)) {
            console.error(
              'Select2: The AJAX results did not return an array in the ' +
              '\`results\` key of the response.'
            );
          }
        }

        callback(results);
      }, function () {
        // Attempt to detect if a request was aborted
        // Only works if the transport exposes a status property
        if ('status' in $request &&
            ($request.status === 0 || $request.status === '0')) {
          return;
        }

        self.trigger('results:message', {
          message: 'errorLoading'
        });
      });

      self._request = $request;
    }

    if (this.ajaxOptions.delay && params.term != null) {
      if (this._queryTimeout) {
        window.clearTimeout(this._queryTimeout);
      }

      this._queryTimeout = window.setTimeout(request, this.ajaxOptions.delay);
    } else {
      request();
    }
  };

  return AjaxAdapter;
});

S2.define('select2/data/tags',[
  'jquery'
], function ($) {
  function Tags (decorated, $element, options) {
    var tags = options.get('tags');

    var createTag = options.get('createTag');

    if (createTag !== undefined) {
      this.createTag = createTag;
    }

    var insertTag = options.get('insertTag');

    if (insertTag !== undefined) {
        this.insertTag = insertTag;
    }

    decorated.call(this, $element, options);

    if (Array.isArray(tags)) {
      for (var t = 0; t < tags.length; t++) {
        var tag = tags[t];
        var item = this._normalizeItem(tag);

        var $option = this.option(item);

        this.$element.append($option);
      }
    }
  }

  Tags.prototype.query = function (decorated, params, callback) {
    var self = this;

    this._removeOldTags();

    if (params.term == null || params.page != null) {
      decorated.call(this, params, callback);
      return;
    }

    function wrapper (obj, child) {
      var data = obj.results;

      for (var i = 0; i < data.length; i++) {
        var option = data[i];

        var checkChildren = (
          option.children != null &&
          !wrapper({
            results: option.children
          }, true)
        );

        var optionText = (option.text || '').toUpperCase();
        var paramsTerm = (params.term || '').toUpperCase();

        var checkText = optionText === paramsTerm;

        if (checkText || checkChildren) {
          if (child) {
            return false;
          }

          obj.data = data;
          callback(obj);

          return;
        }
      }

      if (child) {
        return true;
      }

      var tag = self.createTag(params);

      if (tag != null) {
        var $option = self.option(tag);
        $option.attr('data-select2-tag', 'true');

        self.addOptions([$option]);

        self.insertTag(data, tag);
      }

      obj.results = data;

      callback(obj);
    }

    decorated.call(this, params, wrapper);
  };

  Tags.prototype.createTag = function (decorated, params) {
    if (params.term == null) {
      return null;
    }

    var term = params.term.trim();

    if (term === '') {
      return null;
    }

    return {
      id: term,
      text: term
    };
  };

  Tags.prototype.insertTag = function (_, data, tag) {
    data.unshift(tag);
  };

  Tags.prototype._removeOldTags = function (_) {
    var $options = this.$element.find('option[data-select2-tag]');

    $options.each(function () {
      if (this.selected) {
        return;
      }

      $(this).remove();
    });
  };

  return Tags;
});

S2.define('select2/data/tokenizer',[
  'jquery'
], function ($) {
  function Tokenizer (decorated, $element, options) {
    var tokenizer = options.get('tokenizer');

    if (tokenizer !== undefined) {
      this.tokenizer = tokenizer;
    }

    decorated.call(this, $element, options);
  }

  Tokenizer.prototype.bind = function (decorated, container, $container) {
    decorated.call(this, container, $container);

    this.$search =  container.dropdown.$search || container.selection.$search ||
      $container.find('.select2-search__field');
  };

  Tokenizer.prototype.query = function (decorated, params, callback) {
    var self = this;

    function createAndSelect (data) {
      // Normalize the data object so we can use it for checks
      var item = self._normalizeItem(data);

      // Check if the data object already exists as a tag
      // Select it if it doesn't
      var $existingOptions = self.$element.find('option').filter(function () {
        return $(this).val() === item.id;
      });

      // If an existing option wasn't found for it, create the option
      if (!$existingOptions.length) {
        var $option = self.option(item);
        $option.attr('data-select2-tag', true);

        self._removeOldTags();
        self.addOptions([$option]);
      }

      // Select the item, now that we know there is an option for it
      select(item);
    }

    function select (data) {
      self.trigger('select', {
        data: data
      });
    }

    params.term = params.term || '';

    var tokenData = this.tokenizer(params, this.options, createAndSelect);

    if (tokenData.term !== params.term) {
      // Replace the search term if we have the search box
      if (this.$search.length) {
        this.$search.val(tokenData.term);
        this.$search.trigger('focus');
      }

      params.term = tokenData.term;
    }

    decorated.call(this, params, callback);
  };

  Tokenizer.prototype.tokenizer = function (_, params, options, callback) {
    var separators = options.get('tokenSeparators') || [];
    var term = params.term;
    var i = 0;

    var createTag = this.createTag || function (params) {
      return {
        id: params.term,
        text: params.term
      };
    };

    while (i < term.length) {
      var termChar = term[i];

      if (separators.indexOf(termChar) === -1) {
        i++;

        continue;
      }

      var part = term.substr(0, i);
      var partParams = $.extend({}, params, {
        term: part
      });

      var data = createTag(partParams);

      if (data == null) {
        i++;
        continue;
      }

      callback(data);

      // Reset the term to not include the tokenized portion
      term = term.substr(i + 1) || '';
      i = 0;
    }

    return {
      term: term
    };
  };

  return Tokenizer;
});

S2.define('select2/data/minimumInputLength',[

], function () {
  function MinimumInputLength (decorated, $e, options) {
    this.minimumInputLength = options.get('minimumInputLength');

    decorated.call(this, $e, options);
  }

  MinimumInputLength.prototype.query = function (decorated, params, callback) {
    params.term = params.term || '';

    if (params.term.length < this.minimumInputLength) {
      this.trigger('results:message', {
        message: 'inputTooShort',
        args: {
          minimum: this.minimumInputLength,
          input: params.term,
          params: params
        }
      });

      return;
    }

    decorated.call(this, params, callback);
  };

  return MinimumInputLength;
});

S2.define('select2/data/maximumInputLength',[

], function () {
  function MaximumInputLength (decorated, $e, options) {
    this.maximumInputLength = options.get('maximumInputLength');

    decorated.call(this, $e, options);
  }

  MaximumInputLength.prototype.query = function (decorated, params, callback) {
    params.term = params.term || '';

    if (this.maximumInputLength > 0 &&
        params.term.length > this.maximumInputLength) {
      this.trigger('results:message', {
        message: 'inputTooLong',
        args: {
          maximum: this.maximumInputLength,
          input: params.term,
          params: params
        }
      });

      return;
    }

    decorated.call(this, params, callback);
  };

  return MaximumInputLength;
});

S2.define('select2/data/maximumSelectionLength',[

], function (){
  function MaximumSelectionLength (decorated, $e, options) {
    this.maximumSelectionLength = options.get('maximumSelectionLength');

    decorated.call(this, $e, options);
  }

  MaximumSelectionLength.prototype.bind =
    function (decorated, container, $container) {
      var self = this;

      decorated.call(this, container, $container);

      container.on('select', function () {
        self._checkIfMaximumSelected();
      });
  };

  MaximumSelectionLength.prototype.query =
    function (decorated, params, callback) {
      var self = this;

      this._checkIfMaximumSelected(function () {
        decorated.call(self, params, callback);
      });
  };

  MaximumSelectionLength.prototype._checkIfMaximumSelected =
    function (_, successCallback) {
      var self = this;

      this.current(function (currentData) {
        var count = currentData != null ? currentData.length : 0;
        if (self.maximumSelectionLength > 0 &&
          count >= self.maximumSelectionLength) {
          self.trigger('results:message', {
            message: 'maximumSelected',
            args: {
              maximum: self.maximumSelectionLength
            }
          });
          return;
        }

        if (successCallback) {
          successCallback();
        }
      });
  };

  return MaximumSelectionLength;
});

S2.define('select2/dropdown',[
  'jquery',
  './utils'
], function ($, Utils) {
  function Dropdown ($element, options) {
    this.$element = $element;
    this.options = options;

    Dropdown.__super__.constructor.call(this);
  }

  Utils.Extend(Dropdown, Utils.Observable);

  Dropdown.prototype.render = function () {
    var $dropdown = $(
      '<span class="select2-dropdown">' +
        '<span class="select2-results"></span>' +
      '</span>'
    );

    $dropdown.attr('dir', this.options.get('dir'));

    this.$dropdown = $dropdown;

    return $dropdown;
  };

  Dropdown.prototype.bind = function () {
    // Should be implemented in subclasses
  };

  Dropdown.prototype.position = function ($dropdown, $container) {
    // Should be implemented in subclasses
  };

  Dropdown.prototype.destroy = function () {
    // Remove the dropdown from the DOM
    this.$dropdown.remove();
  };

  return Dropdown;
});

S2.define('select2/dropdown/search',[
  'jquery'
], function ($) {
  function Search () { }

  Search.prototype.render = function (decorated) {
    var $rendered = decorated.call(this);
    var searchLabel = this.options.get('translations').get('search');

    var $search = $(
      '<span class="select2-search select2-search--dropdown">' +
        '<input class="select2-search__field" type="search" tabindex="-1"' +
        ' autocorrect="off" autocapitalize="none"' +
        ' spellcheck="false" role="searchbox" aria-autocomplete="list" />' +
      '</span>'
    );

    this.$searchContainer = $search;
    this.$search = $search.find('input');

    this.$search.prop('autocomplete', this.options.get('autocomplete'));
    this.$search.attr('aria-label', searchLabel());

    $rendered.prepend($search);

    return $rendered;
  };

  Search.prototype.bind = function (decorated, container, $container) {
    var self = this;

    var resultsId = container.id + '-results';

    decorated.call(this, container, $container);

    this.$search.on('keydown', function (evt) {
      self.trigger('keypress', evt);

      self._keyUpPrevented = evt.isDefaultPrevented();
    });

    // Workaround for browsers which do not support the \`input\` event
    // This will prevent double-triggering of events for browsers which support
    // both the \`keyup\` and \`input\` events.
    this.$search.on('input', function (evt) {
      // Unbind the duplicated \`keyup\` event
      $(this).off('keyup');
    });

    this.$search.on('keyup input', function (evt) {
      self.handleSearch(evt);
    });

    container.on('open', function () {
      self.$search.attr('tabindex', 0);
      self.$search.attr('aria-controls', resultsId);

      self.$search.trigger('focus');

      window.setTimeout(function () {
        self.$search.trigger('focus');
      }, 0);
    });

    container.on('close', function () {
      self.$search.attr('tabindex', -1);
      self.$search.removeAttr('aria-controls');
      self.$search.removeAttr('aria-activedescendant');

      self.$search.val('');
      self.$search.trigger('blur');
    });

    container.on('focus', function () {
      if (!container.isOpen()) {
        self.$search.trigger('focus');
      }
    });

    container.on('results:all', function (params) {
      if (params.query.term == null || params.query.term === '') {
        var showSearch = self.showSearch(params);

        if (showSearch) {
          self.$searchContainer[0].classList.remove('select2-search--hide');
        } else {
          self.$searchContainer[0].classList.add('select2-search--hide');
        }
      }
    });

    container.on('results:focus', function (params) {
      if (params.data._resultId) {
        self.$search.attr('aria-activedescendant', params.data._resultId);
      } else {
        self.$search.removeAttr('aria-activedescendant');
      }
    });
  };

  Search.prototype.handleSearch = function (evt) {
    if (!this._keyUpPrevented) {
      var input = this.$search.val();

      this.trigger('query', {
        term: input
      });
    }

    this._keyUpPrevented = false;
  };

  Search.prototype.showSearch = function (_, params) {
    return true;
  };

  return Search;
});

S2.define('select2/dropdown/hidePlaceholder',[

], function () {
  function HidePlaceholder (decorated, $element, options, dataAdapter) {
    this.placeholder = this.normalizePlaceholder(options.get('placeholder'));

    decorated.call(this, $element, options, dataAdapter);
  }

  HidePlaceholder.prototype.append = function (decorated, data) {
    data.results = this.removePlaceholder(data.results);

    decorated.call(this, data);
  };

  HidePlaceholder.prototype.normalizePlaceholder = function (_, placeholder) {
    if (typeof placeholder === 'string') {
      placeholder = {
        id: '',
        text: placeholder
      };
    }

    return placeholder;
  };

  HidePlaceholder.prototype.removePlaceholder = function (_, data) {
    var modifiedData = data.slice(0);

    for (var d = data.length - 1; d >= 0; d--) {
      var item = data[d];

      if (this.placeholder.id === item.id) {
        modifiedData.splice(d, 1);
      }
    }

    return modifiedData;
  };

  return HidePlaceholder;
});

S2.define('select2/dropdown/infiniteScroll',[
  'jquery'
], function ($) {
  function InfiniteScroll (decorated, $element, options, dataAdapter) {
    this.lastParams = {};

    decorated.call(this, $element, options, dataAdapter);

    this.$loadingMore = this.createLoadingMore();
    this.loading = false;
  }

  InfiniteScroll.prototype.append = function (decorated, data) {
    this.$loadingMore.remove();
    this.loading = false;

    decorated.call(this, data);

    if (this.showLoadingMore(data)) {
      this.$results.append(this.$loadingMore);
      this.loadMoreIfNeeded();
    }
  };

  InfiniteScroll.prototype.bind = function (decorated, container, $container) {
    var self = this;

    decorated.call(this, container, $container);

    container.on('query', function (params) {
      self.lastParams = params;
      self.loading = true;
    });

    container.on('query:append', function (params) {
      self.lastParams = params;
      self.loading = true;
    });

    this.$results.on('scroll', this.loadMoreIfNeeded.bind(this));
  };

  InfiniteScroll.prototype.loadMoreIfNeeded = function () {
    var isLoadMoreVisible = $.contains(
      document.documentElement,
      this.$loadingMore[0]
    );

    if (this.loading || !isLoadMoreVisible) {
      return;
    }

    var currentOffset = this.$results.offset().top +
      this.$results.outerHeight(false);
    var loadingMoreOffset = this.$loadingMore.offset().top +
      this.$loadingMore.outerHeight(false);

    if (currentOffset + 50 >= loadingMoreOffset) {
      this.loadMore();
    }
  };

  InfiniteScroll.prototype.loadMore = function () {
    this.loading = true;

    var params = $.extend({}, {page: 1}, this.lastParams);

    params.page++;

    this.trigger('query:append', params);
  };

  InfiniteScroll.prototype.showLoadingMore = function (_, data) {
    return data.pagination && data.pagination.more;
  };

  InfiniteScroll.prototype.createLoadingMore = function () {
    var $option = $(
      '<li ' +
      'class="select2-results__option select2-results__option--load-more"' +
      'role="option" aria-disabled="true"></li>'
    );

    var message = this.options.get('translations').get('loadingMore');

    $option.html(message(this.lastParams));

    return $option;
  };

  return InfiniteScroll;
});

S2.define('select2/dropdown/attachBody',[
  'jquery',
  '../utils'
], function ($, Utils) {
  function AttachBody (decorated, $element, options) {
    this.$dropdownParent = $(options.get('dropdownParent') || document.body);

    decorated.call(this, $element, options);
  }

  AttachBody.prototype.bind = function (decorated, container, $container) {
    var self = this;

    decorated.call(this, container, $container);

    container.on('open', function () {
      self._showDropdown();
      self._attachPositioningHandler(container);

      // Must bind after the results handlers to ensure correct sizing
      self._bindContainerResultHandlers(container);
    });

    container.on('close', function () {
      self._hideDropdown();
      self._detachPositioningHandler(container);
    });

    this.$dropdownContainer.on('mousedown', function (evt) {
      evt.stopPropagation();
    });
  };

  AttachBody.prototype.destroy = function (decorated) {
    decorated.call(this);

    this.$dropdownContainer.remove();
  };

  AttachBody.prototype.position = function (decorated, $dropdown, $container) {
    // Clone all of the container classes
    $dropdown.attr('class', $container.attr('class'));

    $dropdown[0].classList.remove('select2');
    $dropdown[0].classList.add('select2-container--open');

    $dropdown.css({
      position: 'absolute',
      top: -999999
    });

    this.$container = $container;
  };

  AttachBody.prototype.render = function (decorated) {
    var $container = $('<span></span>');

    var $dropdown = decorated.call(this);
    $container.append($dropdown);

    this.$dropdownContainer = $container;

    return $container;
  };

  AttachBody.prototype._hideDropdown = function (decorated) {
    this.$dropdownContainer.detach();
  };

  AttachBody.prototype._bindContainerResultHandlers =
      function (decorated, container) {

    // These should only be bound once
    if (this._containerResultsHandlersBound) {
      return;
    }

    var self = this;

    container.on('results:all', function () {
      self._positionDropdown();
      self._resizeDropdown();
    });

    container.on('results:append', function () {
      self._positionDropdown();
      self._resizeDropdown();
    });

    container.on('results:message', function () {
      self._positionDropdown();
      self._resizeDropdown();
    });

    container.on('select', function () {
      self._positionDropdown();
      self._resizeDropdown();
    });

    container.on('unselect', function () {
      self._positionDropdown();
      self._resizeDropdown();
    });

    this._containerResultsHandlersBound = true;
  };

  AttachBody.prototype._attachPositioningHandler =
      function (decorated, container) {
    var self = this;

    var scrollEvent = 'scroll.select2.' + container.id;
    var resizeEvent = 'resize.select2.' + container.id;
    var orientationEvent = 'orientationchange.select2.' + container.id;

    var $watchers = this.$container.parents().filter(Utils.hasScroll);
    $watchers.each(function () {
      Utils.StoreData(this, 'select2-scroll-position', {
        x: $(this).scrollLeft(),
        y: $(this).scrollTop()
      });
    });

    $watchers.on(scrollEvent, function (ev) {
      var position = Utils.GetData(this, 'select2-scroll-position');
      $(this).scrollTop(position.y);
    });

    $(window).on(scrollEvent + ' ' + resizeEvent + ' ' + orientationEvent,
      function (e) {
      self._positionDropdown();
      self._resizeDropdown();
    });
  };

  AttachBody.prototype._detachPositioningHandler =
      function (decorated, container) {
    var scrollEvent = 'scroll.select2.' + container.id;
    var resizeEvent = 'resize.select2.' + container.id;
    var orientationEvent = 'orientationchange.select2.' + container.id;

    var $watchers = this.$container.parents().filter(Utils.hasScroll);
    $watchers.off(scrollEvent);

    $(window).off(scrollEvent + ' ' + resizeEvent + ' ' + orientationEvent);
  };

  AttachBody.prototype._positionDropdown = function () {
    var $window = $(window);

    var isCurrentlyAbove = this.$dropdown[0].classList
      .contains('select2-dropdown--above');
    var isCurrentlyBelow = this.$dropdown[0].classList
      .contains('select2-dropdown--below');

    var newDirection = null;

    var offset = this.$container.offset();

    offset.bottom = offset.top + this.$container.outerHeight(false);

    var container = {
      height: this.$container.outerHeight(false)
    };

    container.top = offset.top;
    container.bottom = offset.top + container.height;

    var dropdown = {
      height: this.$dropdown.outerHeight(false)
    };

    var viewport = {
      top: $window.scrollTop(),
      bottom: $window.scrollTop() + $window.height()
    };

    var enoughRoomAbove = viewport.top < (offset.top - dropdown.height);
    var enoughRoomBelow = viewport.bottom > (offset.bottom + dropdown.height);

    var css = {
      left: offset.left,
      top: container.bottom
    };

    // Determine what the parent element is to use for calculating the offset
    var $offsetParent = this.$dropdownParent;

    // For statically positioned elements, we need to get the element
    // that is determining the offset
    if ($offsetParent.css('position') === 'static') {
      $offsetParent = $offsetParent.offsetParent();
    }

    var parentOffset = {
      top: 0,
      left: 0
    };

    if (
      $.contains(document.body, $offsetParent[0]) ||
      $offsetParent[0].isConnected
      ) {
      parentOffset = $offsetParent.offset();
    }

    css.top -= parentOffset.top;
    css.left -= parentOffset.left;

    if (!isCurrentlyAbove && !isCurrentlyBelow) {
      newDirection = 'below';
    }

    if (!enoughRoomBelow && enoughRoomAbove && !isCurrentlyAbove) {
      newDirection = 'above';
    } else if (!enoughRoomAbove && enoughRoomBelow && isCurrentlyAbove) {
      newDirection = 'below';
    }

    if (newDirection == 'above' ||
      (isCurrentlyAbove && newDirection !== 'below')) {
      css.top = container.top - parentOffset.top - dropdown.height;
    }

    if (newDirection != null) {
      this.$dropdown[0].classList.remove('select2-dropdown--below');
      this.$dropdown[0].classList.remove('select2-dropdown--above');
      this.$dropdown[0].classList.add('select2-dropdown--' + newDirection);

      this.$container[0].classList.remove('select2-container--below');
      this.$container[0].classList.remove('select2-container--above');
      this.$container[0].classList.add('select2-container--' + newDirection);
    }

    this.$dropdownContainer.css(css);
  };

  AttachBody.prototype._resizeDropdown = function () {
    var css = {
      width: this.$container.outerWidth(false) + 'px'
    };

    if (this.options.get('dropdownAutoWidth')) {
      css.minWidth = css.width;
      css.position = 'relative';
      css.width = 'auto';
    }

    this.$dropdown.css(css);
  };

  AttachBody.prototype._showDropdown = function (decorated) {
    this.$dropdownContainer.appendTo(this.$dropdownParent);

    this._positionDropdown();
    this._resizeDropdown();
  };

  return AttachBody;
});

S2.define('select2/dropdown/minimumResultsForSearch',[

], function () {
  function countResults (data) {
    var count = 0;

    for (var d = 0; d < data.length; d++) {
      var item = data[d];

      if (item.children) {
        count += countResults(item.children);
      } else {
        count++;
      }
    }

    return count;
  }

  function MinimumResultsForSearch (decorated, $element, options, dataAdapter) {
    this.minimumResultsForSearch = options.get('minimumResultsForSearch');

    if (this.minimumResultsForSearch < 0) {
      this.minimumResultsForSearch = Infinity;
    }

    decorated.call(this, $element, options, dataAdapter);
  }

  MinimumResultsForSearch.prototype.showSearch = function (decorated, params) {
    if (countResults(params.data.results) < this.minimumResultsForSearch) {
      return false;
    }

    return decorated.call(this, params);
  };

  return MinimumResultsForSearch;
});

S2.define('select2/dropdown/selectOnClose',[
  '../utils'
], function (Utils) {
  function SelectOnClose () { }

  SelectOnClose.prototype.bind = function (decorated, container, $container) {
    var self = this;

    decorated.call(this, container, $container);

    container.on('close', function (params) {
      self._handleSelectOnClose(params);
    });
  };

  SelectOnClose.prototype._handleSelectOnClose = function (_, params) {
    if (params && params.originalSelect2Event != null) {
      var event = params.originalSelect2Event;

      // Don't select an item if the close event was triggered from a select or
      // unselect event
      if (event._type === 'select' || event._type === 'unselect') {
        return;
      }
    }

    var $highlightedResults = this.getHighlightedResults();

    // Only select highlighted results
    if ($highlightedResults.length < 1) {
      return;
    }

    var data = Utils.GetData($highlightedResults[0], 'data');

    // Don't re-select already selected resulte
    if (
      (data.element != null && data.element.selected) ||
      (data.element == null && data.selected)
    ) {
      return;
    }

    this.trigger('select', {
        data: data
    });
  };

  return SelectOnClose;
});

S2.define('select2/dropdown/closeOnSelect',[

], function () {
  function CloseOnSelect () { }

  CloseOnSelect.prototype.bind = function (decorated, container, $container) {
    var self = this;

    decorated.call(this, container, $container);

    container.on('select', function (evt) {
      self._selectTriggered(evt);
    });

    container.on('unselect', function (evt) {
      self._selectTriggered(evt);
    });
  };

  CloseOnSelect.prototype._selectTriggered = function (_, evt) {
    var originalEvent = evt.originalEvent;

    // Don't close if the control key is being held
    if (originalEvent && (originalEvent.ctrlKey || originalEvent.metaKey)) {
      return;
    }

    this.trigger('close', {
      originalEvent: originalEvent,
      originalSelect2Event: evt
    });
  };

  return CloseOnSelect;
});

S2.define('select2/dropdown/dropdownCss',[
  '../utils'
], function (Utils) {
  function DropdownCSS () { }

  DropdownCSS.prototype.render = function (decorated) {
    var $dropdown = decorated.call(this);

    var dropdownCssClass = this.options.get('dropdownCssClass') || '';

    if (dropdownCssClass.indexOf(':all:') !== -1) {
      dropdownCssClass = dropdownCssClass.replace(':all:', '');

      Utils.copyNonInternalCssClasses($dropdown[0], this.$element[0]);
    }

    $dropdown.addClass(dropdownCssClass);

    return $dropdown;
  };

  return DropdownCSS;
});

S2.define('select2/dropdown/tagsSearchHighlight',[
  '../utils'
], function (Utils) {
  function TagsSearchHighlight () { }

  TagsSearchHighlight.prototype.highlightFirstItem = function (decorated) {
    var $options = this.$results
    .find(
      '.select2-results__option--selectable' +
      ':not(.select2-results__option--selected)'
    );

    if ($options.length > 0) {
      var $firstOption = $options.first();
      var data = Utils.GetData($firstOption[0], 'data');
      var firstElement = data.element;

      if (firstElement && firstElement.getAttribute) {
        if (firstElement.getAttribute('data-select2-tag') === 'true') {
          $firstOption.trigger('mouseenter');

          return;
        }
      }
    }

    decorated.call(this);
  };

  return TagsSearchHighlight;
});

S2.define('select2/i18n/en',[],function () {
  // English
  return {
    errorLoading: function () {
      return 'The results could not be loaded.';
    },
    inputTooLong: function (args) {
      var overChars = args.input.length - args.maximum;

      var message = 'Please delete ' + overChars + ' character';

      if (overChars != 1) {
        message += 's';
      }

      return message;
    },
    inputTooShort: function (args) {
      var remainingChars = args.minimum - args.input.length;

      var message = 'Please enter ' + remainingChars + ' or more characters';

      return message;
    },
    loadingMore: function () {
      return 'Loading more results…';
    },
    maximumSelected: function (args) {
      var message = 'You can only select ' + args.maximum + ' item';

      if (args.maximum != 1) {
        message += 's';
      }

      return message;
    },
    noResults: function () {
      return 'No results found';
    },
    searching: function () {
      return 'Searching…';
    },
    removeAllItems: function () {
      return 'Remove all items';
    },
    removeItem: function () {
      return 'Remove item';
    },
    search: function() {
      return 'Search';
    }
  };
});

S2.define('select2/defaults',[
  'jquery',

  './results',

  './selection/single',
  './selection/multiple',
  './selection/placeholder',
  './selection/allowClear',
  './selection/search',
  './selection/selectionCss',
  './selection/eventRelay',

  './utils',
  './translation',
  './diacritics',

  './data/select',
  './data/array',
  './data/ajax',
  './data/tags',
  './data/tokenizer',
  './data/minimumInputLength',
  './data/maximumInputLength',
  './data/maximumSelectionLength',

  './dropdown',
  './dropdown/search',
  './dropdown/hidePlaceholder',
  './dropdown/infiniteScroll',
  './dropdown/attachBody',
  './dropdown/minimumResultsForSearch',
  './dropdown/selectOnClose',
  './dropdown/closeOnSelect',
  './dropdown/dropdownCss',
  './dropdown/tagsSearchHighlight',

  './i18n/en'
], function ($,

             ResultsList,

             SingleSelection, MultipleSelection, Placeholder, AllowClear,
             SelectionSearch, SelectionCSS, EventRelay,

             Utils, Translation, DIACRITICS,

             SelectData, ArrayData, AjaxData, Tags, Tokenizer,
             MinimumInputLength, MaximumInputLength, MaximumSelectionLength,

             Dropdown, DropdownSearch, HidePlaceholder, InfiniteScroll,
             AttachBody, MinimumResultsForSearch, SelectOnClose, CloseOnSelect,
             DropdownCSS, TagsSearchHighlight,

             EnglishTranslation) {
  function Defaults () {
    this.reset();
  }

  Defaults.prototype.apply = function (options) {
    options = $.extend(true, {}, this.defaults, options);

    if (options.dataAdapter == null) {
      if (options.ajax != null) {
        options.dataAdapter = AjaxData;
      } else if (options.data != null) {
        options.dataAdapter = ArrayData;
      } else {
        options.dataAdapter = SelectData;
      }

      if (options.minimumInputLength > 0) {
        options.dataAdapter = Utils.Decorate(
          options.dataAdapter,
          MinimumInputLength
        );
      }

      if (options.maximumInputLength > 0) {
        options.dataAdapter = Utils.Decorate(
          options.dataAdapter,
          MaximumInputLength
        );
      }

      if (options.maximumSelectionLength > 0) {
        options.dataAdapter = Utils.Decorate(
          options.dataAdapter,
          MaximumSelectionLength
        );
      }

      if (options.tags) {
        options.dataAdapter = Utils.Decorate(options.dataAdapter, Tags);
      }

      if (options.tokenSeparators != null || options.tokenizer != null) {
        options.dataAdapter = Utils.Decorate(
          options.dataAdapter,
          Tokenizer
        );
      }
    }

    if (options.resultsAdapter == null) {
      options.resultsAdapter = ResultsList;

      if (options.ajax != null) {
        options.resultsAdapter = Utils.Decorate(
          options.resultsAdapter,
          InfiniteScroll
        );
      }

      if (options.placeholder != null) {
        options.resultsAdapter = Utils.Decorate(
          options.resultsAdapter,
          HidePlaceholder
        );
      }

      if (options.selectOnClose) {
        options.resultsAdapter = Utils.Decorate(
          options.resultsAdapter,
          SelectOnClose
        );
      }

      if (options.tags) {
        options.resultsAdapter = Utils.Decorate(
          options.resultsAdapter,
          TagsSearchHighlight
        );
      }
    }

    if (options.dropdownAdapter == null) {
      if (options.multiple) {
        options.dropdownAdapter = Dropdown;
      } else {
        var SearchableDropdown = Utils.Decorate(Dropdown, DropdownSearch);

        options.dropdownAdapter = SearchableDropdown;
      }

      if (options.minimumResultsForSearch !== 0) {
        options.dropdownAdapter = Utils.Decorate(
          options.dropdownAdapter,
          MinimumResultsForSearch
        );
      }

      if (options.closeOnSelect) {
        options.dropdownAdapter = Utils.Decorate(
          options.dropdownAdapter,
          CloseOnSelect
        );
      }

      if (options.dropdownCssClass != null) {
        options.dropdownAdapter = Utils.Decorate(
          options.dropdownAdapter,
          DropdownCSS
        );
      }

      options.dropdownAdapter = Utils.Decorate(
        options.dropdownAdapter,
        AttachBody
      );
    }

    if (options.selectionAdapter == null) {
      if (options.multiple) {
        options.selectionAdapter = MultipleSelection;
      } else {
        options.selectionAdapter = SingleSelection;
      }

      // Add the placeholder mixin if a placeholder was specified
      if (options.placeholder != null) {
        options.selectionAdapter = Utils.Decorate(
          options.selectionAdapter,
          Placeholder
        );
      }

      if (options.allowClear) {
        options.selectionAdapter = Utils.Decorate(
          options.selectionAdapter,
          AllowClear
        );
      }

      if (options.multiple) {
        options.selectionAdapter = Utils.Decorate(
          options.selectionAdapter,
          SelectionSearch
        );
      }

      if (options.selectionCssClass != null) {
        options.selectionAdapter = Utils.Decorate(
          options.selectionAdapter,
          SelectionCSS
        );
      }

      options.selectionAdapter = Utils.Decorate(
        options.selectionAdapter,
        EventRelay
      );
    }

    // If the defaults were not previously applied from an element, it is
    // possible for the language option to have not been resolved
    options.language = this._resolveLanguage(options.language);

    // Always fall back to English since it will always be complete
    options.language.push('en');

    var uniqueLanguages = [];

    for (var l = 0; l < options.language.length; l++) {
      var language = options.language[l];

      if (uniqueLanguages.indexOf(language) === -1) {
        uniqueLanguages.push(language);
      }
    }

    options.language = uniqueLanguages;

    options.translations = this._processTranslations(
      options.language,
      options.debug
    );

    return options;
  };

  Defaults.prototype.reset = function () {
    function stripDiacritics (text) {
      // Used 'uni range + named function' from http://jsperf.com/diacritics/18
      function match(a) {
        return DIACRITICS[a] || a;
      }

      return text.replace(/[^\\u0000-\\u007E]/g, match);
    }

    function matcher (params, data) {
      // Always return the object if there is nothing to compare
      if (params.term == null || params.term.trim() === '') {
        return data;
      }

      // Do a recursive check for options with children
      if (data.children && data.children.length > 0) {
        // Clone the data object if there are children
        // This is required as we modify the object to remove any non-matches
        var match = $.extend(true, {}, data);

        // Check each child of the option
        for (var c = data.children.length - 1; c >= 0; c--) {
          var child = data.children[c];

          var matches = matcher(params, child);

          // If there wasn't a match, remove the object in the array
          if (matches == null) {
            match.children.splice(c, 1);
          }
        }

        // If any children matched, return the new object
        if (match.children.length > 0) {
          return match;
        }

        // If there were no matching children, check just the plain object
        return matcher(params, match);
      }

      var original = stripDiacritics(data.text).toUpperCase();
      var term = stripDiacritics(params.term).toUpperCase();

      // Check if the text contains the term
      if (original.indexOf(term) > -1) {
        return data;
      }

      // If it doesn't contain the term, don't return anything
      return null;
    }

    this.defaults = {
      amdLanguageBase: './i18n/',
      autocomplete: 'off',
      closeOnSelect: true,
      debug: false,
      dropdownAutoWidth: false,
      escapeMarkup: Utils.escapeMarkup,
      language: {},
      matcher: matcher,
      minimumInputLength: 0,
      maximumInputLength: 0,
      maximumSelectionLength: 0,
      minimumResultsForSearch: 0,
      selectOnClose: false,
      scrollAfterSelect: false,
      sorter: function (data) {
        return data;
      },
      templateResult: function (result) {
        return result.text;
      },
      templateSelection: function (selection) {
        return selection.text;
      },
      theme: 'default',
      width: 'resolve'
    };
  };

  Defaults.prototype.applyFromElement = function (options, $element) {
    var optionLanguage = options.language;
    var defaultLanguage = this.defaults.language;
    var elementLanguage = $element.prop('lang');
    var parentLanguage = $element.closest('[lang]').prop('lang');

    var languages = Array.prototype.concat.call(
      this._resolveLanguage(elementLanguage),
      this._resolveLanguage(optionLanguage),
      this._resolveLanguage(defaultLanguage),
      this._resolveLanguage(parentLanguage)
    );

    options.language = languages;

    return options;
  };

  Defaults.prototype._resolveLanguage = function (language) {
    if (!language) {
      return [];
    }

    if ($.isEmptyObject(language)) {
      return [];
    }

    if ($.isPlainObject(language)) {
      return [language];
    }

    var languages;

    if (!Array.isArray(language)) {
      languages = [language];
    } else {
      languages = language;
    }

    var resolvedLanguages = [];

    for (var l = 0; l < languages.length; l++) {
      resolvedLanguages.push(languages[l]);

      if (typeof languages[l] === 'string' && languages[l].indexOf('-') > 0) {
        // Extract the region information if it is included
        var languageParts = languages[l].split('-');
        var baseLanguage = languageParts[0];

        resolvedLanguages.push(baseLanguage);
      }
    }

    return resolvedLanguages;
  };

  Defaults.prototype._processTranslations = function (languages, debug) {
    var translations = new Translation();

    for (var l = 0; l < languages.length; l++) {
      var languageData = new Translation();

      var language = languages[l];

      if (typeof language === 'string') {
        try {
          // Try to load it with the original name
          languageData = Translation.loadPath(language);
        } catch (e) {
          try {
            // If we couldn't load it, check if it wasn't the full path
            language = this.defaults.amdLanguageBase + language;
            languageData = Translation.loadPath(language);
          } catch (ex) {
            // The translation could not be loaded at all. Sometimes this is
            // because of a configuration problem, other times this can be
            // because of how Select2 helps load all possible translation files
            if (debug && window.console && console.warn) {
              console.warn(
                'Select2: The language file for "' + language + '" could ' +
                'not be automatically loaded. A fallback will be used instead.'
              );
            }
          }
        }
      } else if ($.isPlainObject(language)) {
        languageData = new Translation(language);
      } else {
        languageData = language;
      }

      translations.extend(languageData);
    }

    return translations;
  };

  Defaults.prototype.set = function (key, value) {
    var camelKey = $.camelCase(key);

    var data = {};
    data[camelKey] = value;

    var convertedData = Utils._convertData(data);

    $.extend(true, this.defaults, convertedData);
  };

  var defaults = new Defaults();

  return defaults;
});

S2.define('select2/options',[
  'jquery',
  './defaults',
  './utils'
], function ($, Defaults, Utils) {
  function Options (options, $element) {
    this.options = options;

    if ($element != null) {
      this.fromElement($element);
    }

    if ($element != null) {
      this.options = Defaults.applyFromElement(this.options, $element);
    }

    this.options = Defaults.apply(this.options);
  }

  Options.prototype.fromElement = function ($e) {
    var excludedData = ['select2'];

    if (this.options.multiple == null) {
      this.options.multiple = $e.prop('multiple');
    }

    if (this.options.disabled == null) {
      this.options.disabled = $e.prop('disabled');
    }

    if (this.options.autocomplete == null && $e.prop('autocomplete')) {
      this.options.autocomplete = $e.prop('autocomplete');
    }

    if (this.options.dir == null) {
      if ($e.prop('dir')) {
        this.options.dir = $e.prop('dir');
      } else if ($e.closest('[dir]').prop('dir')) {
        this.options.dir = $e.closest('[dir]').prop('dir');
      } else {
        this.options.dir = 'ltr';
      }
    }

    $e.prop('disabled', this.options.disabled);
    $e.prop('multiple', this.options.multiple);

    if (Utils.GetData($e[0], 'select2Tags')) {
      if (this.options.debug && window.console && console.warn) {
        console.warn(
          'Select2: The \`data-select2-tags\` attribute has been changed to ' +
          'use the \`data-data\` and \`data-tags="true"\` attributes and will be ' +
          'removed in future versions of Select2.'
        );
      }

      Utils.StoreData($e[0], 'data', Utils.GetData($e[0], 'select2Tags'));
      Utils.StoreData($e[0], 'tags', true);
    }

    if (Utils.GetData($e[0], 'ajaxUrl')) {
      if (this.options.debug && window.console && console.warn) {
        console.warn(
          'Select2: The \`data-ajax-url\` attribute has been changed to ' +
          '\`data-ajax--url\` and support for the old attribute will be removed' +
          ' in future versions of Select2.'
        );
      }

      $e.attr('ajax--url', Utils.GetData($e[0], 'ajaxUrl'));
      Utils.StoreData($e[0], 'ajax-Url', Utils.GetData($e[0], 'ajaxUrl'));
    }

    var dataset = {};

    function upperCaseLetter(_, letter) {
      return letter.toUpperCase();
    }

    // Pre-load all of the attributes which are prefixed with \`data-\`
    for (var attr = 0; attr < $e[0].attributes.length; attr++) {
      var attributeName = $e[0].attributes[attr].name;
      var prefix = 'data-';

      if (attributeName.substr(0, prefix.length) == prefix) {
        // Get the contents of the attribute after \`data-\`
        var dataName = attributeName.substring(prefix.length);

        // Get the data contents from the consistent source
        // This is more than likely the jQuery data helper
        var dataValue = Utils.GetData($e[0], dataName);

        // camelCase the attribute name to match the spec
        var camelDataName = dataName.replace(/-([a-z])/g, upperCaseLetter);

        // Store the data attribute contents into the dataset since
        dataset[camelDataName] = dataValue;
      }
    }

    // Prefer the element's \`dataset\` attribute if it exists
    // jQuery 1.x does not correctly handle data attributes with multiple dashes
    if ($.fn.jquery && $.fn.jquery.substr(0, 2) == '1.' && $e[0].dataset) {
      dataset = $.extend(true, {}, $e[0].dataset, dataset);
    }

    // Prefer our internal data cache if it exists
    var data = $.extend(true, {}, Utils.GetData($e[0]), dataset);

    data = Utils._convertData(data);

    for (var key in data) {
      if (excludedData.indexOf(key) > -1) {
        continue;
      }

      if ($.isPlainObject(this.options[key])) {
        $.extend(this.options[key], data[key]);
      } else {
        this.options[key] = data[key];
      }
    }

    return this;
  };

  Options.prototype.get = function (key) {
    return this.options[key];
  };

  Options.prototype.set = function (key, val) {
    this.options[key] = val;
  };

  return Options;
});

S2.define('select2/core',[
  'jquery',
  './options',
  './utils',
  './keys'
], function ($, Options, Utils, KEYS) {
  var Select2 = function ($element, options) {
    if (Utils.GetData($element[0], 'select2') != null) {
      Utils.GetData($element[0], 'select2').destroy();
    }

    this.$element = $element;

    this.id = this._generateId($element);

    options = options || {};

    this.options = new Options(options, $element);

    Select2.__super__.constructor.call(this);

    // Set up the tabindex

    var tabindex = $element.attr('tabindex') || 0;
    Utils.StoreData($element[0], 'old-tabindex', tabindex);
    $element.attr('tabindex', '-1');

    // Set up containers and adapters

    var DataAdapter = this.options.get('dataAdapter');
    this.dataAdapter = new DataAdapter($element, this.options);

    var $container = this.render();

    this._placeContainer($container);

    var SelectionAdapter = this.options.get('selectionAdapter');
    this.selection = new SelectionAdapter($element, this.options);
    this.$selection = this.selection.render();

    this.selection.position(this.$selection, $container);

    var DropdownAdapter = this.options.get('dropdownAdapter');
    this.dropdown = new DropdownAdapter($element, this.options);
    this.$dropdown = this.dropdown.render();

    this.dropdown.position(this.$dropdown, $container);

    var ResultsAdapter = this.options.get('resultsAdapter');
    this.results = new ResultsAdapter($element, this.options, this.dataAdapter);
    this.$results = this.results.render();

    this.results.position(this.$results, this.$dropdown);

    // Bind events

    var self = this;

    // Bind the container to all of the adapters
    this._bindAdapters();

    // Register any DOM event handlers
    this._registerDomEvents();

    // Register any internal event handlers
    this._registerDataEvents();
    this._registerSelectionEvents();
    this._registerDropdownEvents();
    this._registerResultsEvents();
    this._registerEvents();

    // Set the initial state
    this.dataAdapter.current(function (initialData) {
      self.trigger('selection:update', {
        data: initialData
      });
    });

    // Hide the original select
    $element[0].classList.add('select2-hidden-accessible');
    $element.attr('aria-hidden', 'true');

    // Synchronize any monitored attributes
    this._syncAttributes();

    Utils.StoreData($element[0], 'select2', this);

    // Ensure backwards compatibility with $element.data('select2').
    $element.data('select2', this);
  };

  Utils.Extend(Select2, Utils.Observable);

  Select2.prototype._generateId = function ($element) {
    var id = '';

    if ($element.attr('id') != null) {
      id = $element.attr('id');
    } else if ($element.attr('name') != null) {
      id = $element.attr('name') + '-' + Utils.generateChars(2);
    } else {
      id = Utils.generateChars(4);
    }

    id = id.replace(/(:|\\.|\\[|\\]|,)/g, '');
    id = 'select2-' + id;

    return id;
  };

  Select2.prototype._placeContainer = function ($container) {
    $container.insertAfter(this.$element);

    var width = this._resolveWidth(this.$element, this.options.get('width'));

    if (width != null) {
      $container.css('width', width);
    }
  };

  Select2.prototype._resolveWidth = function ($element, method) {
    var WIDTH = /^width:(([-+]?([0-9]*\\.)?[0-9]+)(px|em|ex|%|in|cm|mm|pt|pc))/i;

    if (method == 'resolve') {
      var styleWidth = this._resolveWidth($element, 'style');

      if (styleWidth != null) {
        return styleWidth;
      }

      return this._resolveWidth($element, 'element');
    }

    if (method == 'element') {
      var elementWidth = $element.outerWidth(false);

      if (elementWidth <= 0) {
        return 'auto';
      }

      return elementWidth + 'px';
    }

    if (method == 'style') {
      var style = $element.attr('style');

      if (typeof(style) !== 'string') {
        return null;
      }

      var attrs = style.split(';');

      for (var i = 0, l = attrs.length; i < l; i = i + 1) {
        var attr = attrs[i].replace(/\\s/g, '');
        var matches = attr.match(WIDTH);

        if (matches !== null && matches.length >= 1) {
          return matches[1];
        }
      }

      return null;
    }

    if (method == 'computedstyle') {
      var computedStyle = window.getComputedStyle($element[0]);

      return computedStyle.width;
    }

    return method;
  };

  Select2.prototype._bindAdapters = function () {
    this.dataAdapter.bind(this, this.$container);
    this.selection.bind(this, this.$container);

    this.dropdown.bind(this, this.$container);
    this.results.bind(this, this.$container);
  };

  Select2.prototype._registerDomEvents = function () {
    var self = this;

    this.$element.on('change.select2', function () {
      self.dataAdapter.current(function (data) {
        self.trigger('selection:update', {
          data: data
        });
      });
    });

    this.$element.on('focus.select2', function (evt) {
      self.trigger('focus', evt);
    });

    this._syncA = Utils.bind(this._syncAttributes, this);
    this._syncS = Utils.bind(this._syncSubtree, this);

    this._observer = new window.MutationObserver(function (mutations) {
      self._syncA();
      self._syncS(mutations);
    });
    this._observer.observe(this.$element[0], {
      attributes: true,
      childList: true,
      subtree: false
    });
  };

  Select2.prototype._registerDataEvents = function () {
    var self = this;

    this.dataAdapter.on('*', function (name, params) {
      self.trigger(name, params);
    });
  };

  Select2.prototype._registerSelectionEvents = function () {
    var self = this;
    var nonRelayEvents = ['toggle', 'focus'];

    this.selection.on('toggle', function () {
      self.toggleDropdown();
    });

    this.selection.on('focus', function (params) {
      self.focus(params);
    });

    this.selection.on('*', function (name, params) {
      if (nonRelayEvents.indexOf(name) !== -1) {
        return;
      }

      self.trigger(name, params);
    });
  };

  Select2.prototype._registerDropdownEvents = function () {
    var self = this;

    this.dropdown.on('*', function (name, params) {
      self.trigger(name, params);
    });
  };

  Select2.prototype._registerResultsEvents = function () {
    var self = this;

    this.results.on('*', function (name, params) {
      self.trigger(name, params);
    });
  };

  Select2.prototype._registerEvents = function () {
    var self = this;

    this.on('open', function () {
      self.$container[0].classList.add('select2-container--open');
    });

    this.on('close', function () {
      self.$container[0].classList.remove('select2-container--open');
    });

    this.on('enable', function () {
      self.$container[0].classList.remove('select2-container--disabled');
    });

    this.on('disable', function () {
      self.$container[0].classList.add('select2-container--disabled');
    });

    this.on('blur', function () {
      self.$container[0].classList.remove('select2-container--focus');
    });

    this.on('query', function (params) {
      if (!self.isOpen()) {
        self.trigger('open', {});
      }

      this.dataAdapter.query(params, function (data) {
        self.trigger('results:all', {
          data: data,
          query: params
        });
      });
    });

    this.on('query:append', function (params) {
      this.dataAdapter.query(params, function (data) {
        self.trigger('results:append', {
          data: data,
          query: params
        });
      });
    });

    this.on('keypress', function (evt) {
      var key = evt.which;

      if (self.isOpen()) {
        if (key === KEYS.ESC || (key === KEYS.UP && evt.altKey)) {
          self.close(evt);

          evt.preventDefault();
        } else if (key === KEYS.ENTER || key === KEYS.TAB) {
          self.trigger('results:select', {});

          evt.preventDefault();
        } else if ((key === KEYS.SPACE && evt.ctrlKey)) {
          self.trigger('results:toggle', {});

          evt.preventDefault();
        } else if (key === KEYS.UP) {
          self.trigger('results:previous', {});

          evt.preventDefault();
        } else if (key === KEYS.DOWN) {
          self.trigger('results:next', {});

          evt.preventDefault();
        }
      } else {
        if (key === KEYS.ENTER || key === KEYS.SPACE ||
            (key === KEYS.DOWN && evt.altKey)) {
          self.open();

          evt.preventDefault();
        }
      }
    });
  };

  Select2.prototype._syncAttributes = function () {
    this.options.set('disabled', this.$element.prop('disabled'));

    if (this.isDisabled()) {
      if (this.isOpen()) {
        this.close();
      }

      this.trigger('disable', {});
    } else {
      this.trigger('enable', {});
    }
  };

  Select2.prototype._isChangeMutation = function (mutations) {
    var self = this;

    if (mutations.addedNodes && mutations.addedNodes.length > 0) {
      for (var n = 0; n < mutations.addedNodes.length; n++) {
        var node = mutations.addedNodes[n];

        if (node.selected) {
          return true;
        }
      }
    } else if (mutations.removedNodes && mutations.removedNodes.length > 0) {
      return true;
    } else if (Array.isArray(mutations)) {
      return mutations.some(function (mutation) {
        return self._isChangeMutation(mutation);
      });
    }

    return false;
  };

  Select2.prototype._syncSubtree = function (mutations) {
    var changed = this._isChangeMutation(mutations);
    var self = this;

    // Only re-pull the data if we think there is a change
    if (changed) {
      this.dataAdapter.current(function (currentData) {
        self.trigger('selection:update', {
          data: currentData
        });
      });
    }
  };

  /**
   * Override the trigger method to automatically trigger pre-events when
   * there are events that can be prevented.
   */
  Select2.prototype.trigger = function (name, args) {
    var actualTrigger = Select2.__super__.trigger;
    var preTriggerMap = {
      'open': 'opening',
      'close': 'closing',
      'select': 'selecting',
      'unselect': 'unselecting',
      'clear': 'clearing'
    };

    if (args === undefined) {
      args = {};
    }

    if (name in preTriggerMap) {
      var preTriggerName = preTriggerMap[name];
      var preTriggerArgs = {
        prevented: false,
        name: name,
        args: args
      };

      actualTrigger.call(this, preTriggerName, preTriggerArgs);

      if (preTriggerArgs.prevented) {
        args.prevented = true;

        return;
      }
    }

    actualTrigger.call(this, name, args);
  };

  Select2.prototype.toggleDropdown = function () {
    if (this.isDisabled()) {
      return;
    }

    if (this.isOpen()) {
      this.close();
    } else {
      this.open();
    }
  };

  Select2.prototype.open = function () {
    if (this.isOpen()) {
      return;
    }

    if (this.isDisabled()) {
      return;
    }

    this.trigger('query', {});
  };

  Select2.prototype.close = function (evt) {
    if (!this.isOpen()) {
      return;
    }

    this.trigger('close', { originalEvent : evt });
  };

  /**
   * Helper method to abstract the "enabled" (not "disabled") state of this
   * object.
   *
   * @return {true} if the instance is not disabled.
   * @return {false} if the instance is disabled.
   */
  Select2.prototype.isEnabled = function () {
    return !this.isDisabled();
  };

  /**
   * Helper method to abstract the "disabled" state of this object.
   *
   * @return {true} if the disabled option is true.
   * @return {false} if the disabled option is false.
   */
  Select2.prototype.isDisabled = function () {
    return this.options.get('disabled');
  };

  Select2.prototype.isOpen = function () {
    return this.$container[0].classList.contains('select2-container--open');
  };

  Select2.prototype.hasFocus = function () {
    return this.$container[0].classList.contains('select2-container--focus');
  };

  Select2.prototype.focus = function (data) {
    // No need to re-trigger focus events if we are already focused
    if (this.hasFocus()) {
      return;
    }

    this.$container[0].classList.add('select2-container--focus');
    this.trigger('focus', {});
  };

  Select2.prototype.enable = function (args) {
    if (this.options.get('debug') && window.console && console.warn) {
      console.warn(
        'Select2: The \`select2("enable")\` method has been deprecated and will' +
        ' be removed in later Select2 versions. Use $element.prop("disabled")' +
        ' instead.'
      );
    }

    if (args == null || args.length === 0) {
      args = [true];
    }

    var disabled = !args[0];

    this.$element.prop('disabled', disabled);
  };

  Select2.prototype.data = function () {
    if (this.options.get('debug') &&
        arguments.length > 0 && window.console && console.warn) {
      console.warn(
        'Select2: Data can no longer be set using \`select2("data")\`. You ' +
        'should consider setting the value instead using \`$element.val()\`.'
      );
    }

    var data = [];

    this.dataAdapter.current(function (currentData) {
      data = currentData;
    });

    return data;
  };

  Select2.prototype.val = function (args) {
    if (this.options.get('debug') && window.console && console.warn) {
      console.warn(
        'Select2: The \`select2("val")\` method has been deprecated and will be' +
        ' removed in later Select2 versions. Use $element.val() instead.'
      );
    }

    if (args == null || args.length === 0) {
      return this.$element.val();
    }

    var newVal = args[0];

    if (Array.isArray(newVal)) {
      newVal = newVal.map(function (obj) {
        return obj.toString();
      });
    }

    this.$element.val(newVal).trigger('input').trigger('change');
  };

  Select2.prototype.destroy = function () {
    Utils.RemoveData(this.$container[0]);
    this.$container.remove();

    this._observer.disconnect();
    this._observer = null;

    this._syncA = null;
    this._syncS = null;

    this.$element.off('.select2');
    this.$element.attr('tabindex',
    Utils.GetData(this.$element[0], 'old-tabindex'));

    this.$element[0].classList.remove('select2-hidden-accessible');
    this.$element.attr('aria-hidden', 'false');
    Utils.RemoveData(this.$element[0]);
    this.$element.removeData('select2');

    this.dataAdapter.destroy();
    this.selection.destroy();
    this.dropdown.destroy();
    this.results.destroy();

    this.dataAdapter = null;
    this.selection = null;
    this.dropdown = null;
    this.results = null;
  };

  Select2.prototype.render = function () {
    var $container = $(
      '<span class="select2 select2-container">' +
        '<span class="selection"></span>' +
        '<span class="dropdown-wrapper" aria-hidden="true"></span>' +
      '</span>'
    );

    $container.attr('dir', this.options.get('dir'));

    this.$container = $container;

    this.$container[0].classList
      .add('select2-container--' + this.options.get('theme'));

    Utils.StoreData($container[0], 'element', this.$element);

    return $container;
  };

  return Select2;
});

S2.define('jquery-mousewheel',[
  'jquery'
], function ($) {
  // Used to shim jQuery.mousewheel for non-full builds.
  return $;
});

S2.define('jquery.select2',[
  'jquery',
  'jquery-mousewheel',

  './select2/core',
  './select2/defaults',
  './select2/utils'
], function ($, _, Select2, Defaults, Utils) {
  if ($.fn.select2 == null) {
    // All methods that should return the element
    var thisMethods = ['open', 'close', 'destroy'];

    $.fn.select2 = function (options) {
      options = options || {};

      if (typeof options === 'object') {
        this.each(function () {
          var instanceOptions = $.extend(true, {}, options);

          var instance = new Select2($(this), instanceOptions);
        });

        return this;
      } else if (typeof options === 'string') {
        var ret;
        var args = Array.prototype.slice.call(arguments, 1);

        this.each(function () {
          var instance = Utils.GetData(this, 'select2');

          if (instance == null && window.console && console.error) {
            console.error(
              'The select2(\\'' + options + '\\') method was called on an ' +
              'element that is not using Select2.'
            );
          }

          ret = instance[options].apply(instance, args);
        });

        // Check if we should be returning \`this\`
        if (thisMethods.indexOf(options) > -1) {
          return this;
        }

        return ret;
      } else {
        throw new Error('Invalid arguments for Select2: ' + options);
      }
    };
  }

  if ($.fn.select2.defaults == null) {
    $.fn.select2.defaults = Defaults;
  }

  return Select2;
});

  // Return the AMD loader configuration so it can be used outside of this file
  return {
    define: S2.define,
    require: S2.require
  };
}());

  // Autoload the jQuery bindings
  // We know that all of the modules exist above this, so we're safe
  var select2 = S2.require('jquery.select2');

  // Hold the AMD module references on the jQuery function that was just loaded
  // This allows Select2 to use the internal loader outside of this file, such
  // as in the language files.
  jQuery.fn.select2.amd = S2;

  // Return the Select2 instance for anyone who is importing it.
  return select2;
}));
`;new Function("module","require","window","jQuery",Ts)({},()=>G,window,G);function $s(){G(".fos-select2").select2({placeholder:"Select a fos"})}function Is(){G(document).on("click","#form_reset_button",function(){Os(G("#filter_form"))}),G("#expand_button").click(function(){G("#collapseOne").collapse(),G("#plus_minus").toggleClass("fa-plus fa-minus")});const t=[["selectAll","attributeform-"],["selectAllAllocations","allocationform-"],["selectAll","userform-"],["selectAll","users"],["selectAll","noteform-"],["selectAll","grantform-"],["selectAll","pubform-"],["selectAll","grantdownloadform-"]];for(const i of t)G("#"+i[0]).click(function(){G("input[name^='"+i[1]+"']").prop("checked",G(this).prop("checked"))}),G("input[name^='"+i[1]+"']").click(function(){G(this).attr("id")!=i[0]&&G("#"+i[0]).prop("checked",!1)})}function Os(t){t.find("input:text, input:password, input:file, select, textarea").val(""),t.find("input:radio, input:checkbox").removeAttr("checked").removeAttr("selected")}function Ns(){const t=document.querySelectorAll("div.table-responsive > table.datatable");for(const e of t)e!==null&&new Ka(e,{pageLength:10,orderClasses:!1,order:[[1,"desc"]]});const i=document.querySelectorAll("div.table-responsive > table.datatable-long");for(const e of i)e!==null&&new Ka(e,{pageLength:50,orderClasses:!1,order:[[1,"desc"]]})}Object.assign(window,{getCookie:function(t){Mo(t)},drawGauges:function(t){No(t)},$:G,jQuery:G});function ti(){for(const t of[As,$s,Is,Ns])t()}document.readyState!=="loading"?ti():document.addEventListener("DOMContentLoaded",ti);
