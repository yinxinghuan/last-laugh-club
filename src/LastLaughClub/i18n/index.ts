import type { Copy, Locale } from '../types';
const common = {
  zh:{anthology:'三个故事 · 一种反转',titleTop:'最后笑的',titleBottom:'是你',deck:'他们已经判定你输了。选一个最不像答案的答案。',start:'开始第一段',choose:'你替她怎么做？',loading:'正在接上下一镜…',passed:'他们改口了',failed:'他们更相信她了',retry:'换个答案',soundOn:'关闭声音',soundOff:'打开声音',watermark:'AlterU'},
  en:{anthology:'THREE STORIES · ONE REVERSAL',titleTop:'THE LAST',titleBottom:'LAUGH',deck:'THEY ALREADY DECIDED YOU LOST. PICK THE ANSWER THAT SHOULD NOT WORK.',start:'START STORY ONE',choose:'WHAT DO YOU DO?',loading:'CONNECTING THE NEXT SHOT…',passed:'THE ROOM CHANGED ITS MIND',failed:'THEY BELIEVE HER EVEN MORE',retry:'TRY ANOTHER ANSWER',soundOn:'Mute sound',soundOff:'Enable sound',watermark:'AlterU'},
} as const;
export function detectLocale():Locale { const override=localStorage.getItem('game_locale'); if(override==='zh'||override==='en')return override; return navigator.language.toLowerCase().startsWith('zh')?'zh':'en'; }
export function createTranslator(locale:Locale){ return (key:keyof typeof common.zh)=>common[locale][key]; }
export function localize(copy:Copy,locale:Locale){ return copy[locale]; }
