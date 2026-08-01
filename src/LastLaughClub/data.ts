import type { Sketch } from './types';
export const sketches:Sketch[]=[{
  id:'champagne_witness',number:1,mediaDir:'sketch1',setupVideoTime:5,
  label:{zh:'故事 1 / 被诬陷',en:'STORY 1 / FALSELY ACCUSED'},
  setupCaption:{zh:'十秒前，你只是把酒送到她面前。',en:'TEN SECONDS AGO, YOU SIMPLY SERVED HER A DRINK.'},
  conflict:{zh:'她说你偷了订婚戒指',en:'SHE SAYS YOU STOLE HER RING'},
  question:{zh:'经理倒空你的小费袋，所有人都在拍。',en:'THE MANAGER EMPTIES YOUR TIPS. EVERY PHONE IS ON YOU.'},
  choiceAlt:{zh:'Elena 被当众指控偷戒指，经理倒空她的小费袋',en:'Elena is publicly accused while her manager empties her tip pouch'},
  nextLabel:{zh:'进入下一个故事',en:'ENTER THE NEXT STORY'},reclaimed:{zh:'清白',en:'INNOCENCE'},
  outcomes:[
    {id:'empty_pockets',success:false,videoTime:5,label:{zh:'把所有口袋翻给他们看',en:'TURN OUT EVERY POCKET'},resultTitle:{zh:'清白没有让他们停下手机',en:'INNOCENCE DID NOT LOWER THEIR PHONES'},resultDetail:{zh:'口袋是空的，经理还是指向了出口。',en:'YOUR POCKETS ARE EMPTY. THE MANAGER STILL POINTS TO THE EXIT.'}},
    {id:'search_floor',success:false,videoTime:5,label:{zh:'跪下帮她找“丢失”的戒指',en:'GET DOWN AND SEARCH FOR IT'},resultTitle:{zh:'他们把你的忍让当成心虚',en:'THEY MISTOOK HUMILITY FOR GUILT'},resultDetail:{zh:'你在地上找，她举着藏有戒指的酒杯。',en:'YOU SEARCH THE FLOOR. SHE HOLDS THE GLASS THAT HIDES IT.'}},
    {id:'champagne_testifies',success:true,videoTime:5,label:{zh:'让香槟自己作证',en:'MAKE THE CHAMPAGNE TESTIFY'},resultTitle:{zh:'戒指从她自己的酒杯里跳了出来',en:'THE RING JUMPED OUT OF HER OWN GLASS'},resultDetail:{zh:'镜头转向证物和 Olivia，经理当众向你道歉。',en:'THE CAMERAS FIND THE PROOF. THE MANAGER APOLOGIZES IN PUBLIC.'}},
  ]
},{
  id:'rain_review',number:2,mediaDir:'sketch2',setupVideoTime:5,
  label:{zh:'故事 2 / 被看低',en:'STORY 2 / LOOKED DOWN ON'},
  setupCaption:{zh:'她看了你的裙子一眼，就决定你不配进来。',en:'ONE LOOK AT YOUR DRESS—AND SHE DECIDED YOU DID NOT BELONG.'},
  conflict:{zh:'她故意把香槟泼在你的作品上',en:'SHE POURED CHAMPAGNE ON YOUR WORK'},
  question:{zh:'摄影师在笑，通行证也被收了回去。',en:'THE CAMERAS ARE LAUGHING. YOUR PASS IS PULLED BACK.'},
  choiceAlt:{zh:'Mara 的手工礼服被泼污，时装编辑当众嘲笑她',en:'Mara’s handmade gown is stained while the fashion editor mocks her'},
  nextLabel:{zh:'进入最后一个故事',en:'ENTER THE FINAL STORY'},reclaimed:{zh:'资格',en:'BELONGING'},
  outcomes:[
    {id:'hide_with_coat',success:false,videoTime:5,label:{zh:'用外套把污渍遮起来',en:'HIDE IT UNDER A COAT'},resultTitle:{zh:'她顺手把你当成了衣帽间员工',en:'SHE MISTOOK YOU FOR COAT CHECK'},resultDetail:{zh:'你遮住了作品，也遮住了自己来这里的理由。',en:'YOU HID THE DRESS—AND THE REASON YOU BELONGED.'}},
    {id:'splash_back',success:false,videoTime:5,label:{zh:'把香槟原样泼回去',en:'THROW THE CHAMPAGNE BACK'},resultTitle:{zh:'她毁了裙子，你却成了麻烦',en:'SHE RUINED THE DRESS. YOU BECAME THE PROBLEM.'},resultDetail:{zh:'Leo 抬手叫停，前排通行证离你更远。',en:'LEO STOPS YOU. THE FRONT-ROW PASS MOVES FARTHER AWAY.'}},
    {id:'rain_reviews',success:true,videoTime:5,label:{zh:'让雨来评价这条裙子',en:'LET THE RAIN REVIEW THE DRESS'},resultTitle:{zh:'你的布料在雨里开花了',en:'YOUR FABRIC BLOOMED IN THE RAIN'},resultDetail:{zh:'污渍消失，所有摄影机转向你，通行证重新递了过来。',en:'THE STAIN VANISHES. EVERY CAMERA TURNS. THE PASS COMES BACK.'}},
  ]
},{
  id:'music_box_vote',number:3,mediaDir:'sketch3',setupVideoTime:5,
  label:{zh:'故事 3 / 被抹去',en:'STORY 3 / ERASED'},
  setupCaption:{zh:'这是你女儿的婚礼，也是你们约好的那支舞。',en:'IT IS YOUR DAUGHTER’S WEDDING—AND THE DANCE YOU PROMISED.'},
  conflict:{zh:'他把你从父女舞里拿掉了',en:'HE REMOVED YOU FROM THE FATHER-DAUGHTER DANCE'},
  question:{zh:'理由只是：你的旧西装会破坏照片。',en:'BECAUSE YOUR OLD SUIT WOULD “RUIN THE PHOTOS.”'},
  choiceAlt:{zh:'富裕继父拿走父女舞名卡，Luis 被当众排除',en:'The wealthy stepfather takes the dance card and excludes Luis'},
  nextLabel:{zh:'重看三个故事',en:'REPLAY ALL THREE STORIES'},reclaimed:{zh:'父亲',en:'FATHER'},
  outcomes:[
    {id:'shout_father',success:false,videoTime:5,label:{zh:'大喊：“我才是她亲生父亲！”',en:'SHOUT: “I AM HER REAL FATHER!”'},resultTitle:{zh:'你说出了事实，却刺痛了她',en:'YOU SPOKE THE TRUTH—AND HURT HER'},resultDetail:{zh:'Emma 当场落泪，Richard 更像那个冷静的人。',en:'EMMA BREAKS DOWN. RICHARD LOOKS LIKE THE CALM ONE.'}},
    {id:'leave_quietly',success:false,videoTime:5,label:{zh:'拿着音乐盒悄悄离开',en:'TAKE THE MUSIC BOX AND LEAVE'},resultTitle:{zh:'你退出了本来属于你们的舞',en:'YOU LEFT THE DANCE THAT WAS YOURS'},resultDetail:{zh:'聚光灯照向 Richard，你和共同记忆一起退场。',en:'THE SPOTLIGHT FINDS RICHARD. YOUR SHARED MEMORY LEAVES WITH YOU.'}},
    {id:'music_box_chooses',success:true,videoTime:10,label:{zh:'让旧音乐盒选择她的舞伴',en:'LET THE OLD MUSIC BOX CHOOSE'},resultTitle:{zh:'她听出了小时候的那首歌',en:'SHE REMEMBERED THE SONG FROM CHILDHOOD'},resultDetail:{zh:'Emma 穿过人群牵起你的手，全场重新承认了这支父女舞。',en:'EMMA CROSSES THE ROOM, TAKES YOUR HAND, AND RESTORES YOUR DANCE.'}},
  ]
}];
