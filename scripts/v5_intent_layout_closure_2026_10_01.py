# -*- coding: utf-8 -*-
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MARK='V5 intent detail layout closure — 2026-10-01'
CSS=r'''
/* V5 intent detail layout closure — 2026-10-01 */
.intent-detail .article-hero .wrap{
  width:min(100%,980px);
}
.intent-detail .article-hero{
  text-align:left;
}
.intent-detail .article-hero h1{
  max-width:900px;
}
.intent-detail .article-deck{
  max-width:760px;
}
.intent-detail .article-cover{
  width:min(calc(100% - 2 * var(--gutter)),1120px);
  height:clamp(320px,48vw,610px);
}
.intent-detail .article-layout{
  grid-template-columns:minmax(0,780px);
  gap:0;
  justify-content:center;
}
.intent-detail .article-body{
  width:100%;
  max-width:780px;
  color:var(--ink-soft);
  font-size:16.5px;
  line-height:1.82;
}
.intent-detail .article-body>p{
  margin:0 0 20px;
}
.intent-detail .article-body>ul{
  margin:0 0 28px;
  padding-left:22px;
}
.intent-detail .article-body li{
  margin:0 0 8px;
}
.intent-detail .article-body h2{
  margin:58px 0 18px;
  font-size:clamp(34px,4.2vw,44px);
  line-height:1.06;
}
.intent-detail .article-body h3{
  margin:0 0 10px;
  font-size:27px;
}
.intent-detail .verdict{
  margin:0 0 38px;
  padding:30px 32px;
  background:var(--ink);
  color:var(--white);
}
.intent-detail .verdict .label{
  display:block;
  margin-bottom:11px;
  color:#f7c966;
  font-size:10px;
  font-weight:700;
  letter-spacing:.16em;
  text-transform:uppercase;
}
.intent-detail .verdict p{
  margin:0!important;
  color:var(--white)!important;
  font-family:var(--serif);
  font-size:clamp(22px,2.6vw,28px);
  line-height:1.45;
}
.intent-detail .fact-grid{
  display:grid;
  grid-template-columns:repeat(3,minmax(0,1fr));
  gap:10px;
  margin:0 0 42px;
}
.intent-detail .fact{
  min-height:142px;
  padding:20px;
  border:1px solid var(--line);
  background:rgba(255,253,248,.42);
}
.intent-detail .fact b{
  display:block;
  margin-bottom:8px;
  color:var(--ink);
  font-family:var(--serif);
  font-size:24px;
  font-weight:500;
  line-height:1.08;
}
.intent-detail .fact span{
  display:block;
  color:var(--ink-soft);
  font-size:12px;
  line-height:1.55;
}
.intent-detail .place{
  margin:14px 0;
  padding:24px 26px;
  border:1px solid var(--line);
  background:rgba(255,253,248,.32);
}
.intent-detail .place .address{
  margin-bottom:9px;
  color:var(--blue-deep);
  font-size:10px;
  font-weight:700;
  letter-spacing:.14em;
  text-transform:uppercase;
}
.intent-detail .place h3{
  margin:0 0 9px;
}
.intent-detail .place p{
  margin:0 0 12px;
}
.intent-detail .place p:last-of-type{
  margin-bottom:0;
}
.intent-detail .place>a{
  display:inline-block;
  margin-top:14px;
  font-size:11px;
  font-weight:700;
  letter-spacing:.08em;
  text-transform:uppercase;
}
.intent-detail .note,
.intent-detail .culture-practical{
  margin:32px 0;
  padding:23px 25px;
  border-left:3px solid var(--blue);
  background:rgba(23,111,131,.07);
  color:var(--ink);
}
.intent-detail .note{
  font-size:14px;
  line-height:1.65;
}
.intent-detail .culture-practical>span{
  display:block;
  margin-bottom:9px;
  color:var(--blue-deep);
  font-size:9px;
  font-weight:700;
  letter-spacing:.15em;
  text-transform:uppercase;
}
.intent-detail .culture-practical p{
  margin:0!important;
  color:var(--ink)!important;
  font-size:14px;
  line-height:1.65;
}
.intent-detail .sources{
  margin-top:58px;
  padding-top:25px;
  border-top:1px solid var(--line);
}
.intent-detail .sources h2{
  margin:0 0 14px;
  color:var(--blue-deep);
  font-family:var(--sans);
  font-size:10px;
  font-weight:700;
  letter-spacing:.15em;
  text-transform:uppercase;
}
.intent-detail .sources ul{
  margin:0;
  padding-left:18px;
}
.intent-detail .sources li{
  margin-bottom:7px;
  color:var(--ink-soft);
  font-size:12px;
  line-height:1.55;
}
.intent-detail .sources a{
  text-decoration:underline;
  text-underline-offset:3px;
}
.intent-detail .article-body .button{
  color:var(--white);
  text-decoration:none;
}
.intent-detail .article-body .button:hover,
.intent-detail .article-body .button:focus-visible{
  color:var(--white);
}
@media(max-width:760px){
  .intent-detail .article-hero{
    padding:48px 0 36px;
  }
  .intent-detail .article-hero h1{
    font-size:clamp(42px,12vw,62px);
    line-height:.98;
  }
  .intent-detail .article-deck{
    margin-top:20px;
    font-size:20px!important;
    line-height:1.45!important;
  }
  .intent-detail .article-cover{
    width:100%;
    height:clamp(250px,72vw,420px);
  }
  .intent-detail .v3-section{
    padding:40px 0 58px;
  }
  .intent-detail .article-layout{
    display:block;
  }
  .intent-detail .article-body{
    max-width:none;
    font-size:16px;
    line-height:1.76;
  }
  .intent-detail .article-body h2{
    margin-top:46px;
    font-size:34px;
  }
  .intent-detail .fact-grid{
    grid-template-columns:1fr;
    gap:8px;
    margin-bottom:34px;
  }
  .intent-detail .fact{
    min-height:0;
    padding:18px;
  }
  .intent-detail .place{
    margin:10px 0;
    padding:20px;
  }
  .intent-detail .verdict{
    padding:24px;
    margin-bottom:30px;
  }
  .intent-detail .note,
  .intent-detail .culture-practical{
    margin:26px 0;
    padding:20px;
  }
  .intent-detail .sources{
    margin-top:46px;
  }
}
'''
for rel in ('assets/v3.css','assets/site.css'):
    p=ROOT/rel
    if not p.exists():
        continue
    s=p.read_text(encoding='utf-8')
    if MARK not in s:
        p.write_text(s.rstrip()+'\n\n'+CSS.strip()+'\n',encoding='utf-8')
        print('styled',rel)
