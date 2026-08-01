export type Locale = 'zh' | 'en';
export type Copy = { zh: string; en: string };
export type Phase = 'cover' | 'setup' | 'question' | 'performance' | 'verdict';
export type Outcome = { id:string; success:boolean; videoTime:5|10; label:Copy; resultTitle:Copy; resultDetail:Copy };
export type Sketch = { id:string; number:number; mediaDir:string; setupVideoTime:5; label:Copy; setupCaption:Copy; conflict:Copy; question:Copy; choiceAlt:Copy; nextLabel:Copy; reclaimed:Copy; outcomes:[Outcome,Outcome,Outcome] };
