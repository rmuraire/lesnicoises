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
.intent-detail .trend-2026{
  margin:62px 0 0;
  padding-top:34px;
  border-top:2px solid var(--ink);
}
.intent-detail .trend-2026>.eyebrow{
  margin-bottom:8px!important;
  color:var(--blue-deep)!important;
  font-size:9px!important;
  font-weight:800!important;
  letter-spacing:.16em!important;
  text-transform:uppercase;
}
.intent-detail .trend-2026>h2{
  margin-top:0;
}
.intent-detail .trend-alert{
  margin:24px 0 28px;
  padding:24px 26px;
  background:#f4ecdc;
  border:1px solid rgba(20,33,61,.14);
}
.intent-detail .trend-alert>strong{
  display:block;
  margin-bottom:8px;
  color:var(--ink);
  font-family:var(--serif);
  font-size:20px;
  font-weight:500;
  line-height:1.25;
}
.intent-detail .trend-alert p{
  margin:0!important;
  color:var(--ink-soft)!important;
  font-size:14px;
  line-height:1.65;
}
.intent-detail .scouting-grid{
  display:grid;
  grid-template-columns:repeat(3,minmax(0,1fr));
  gap:10px;
  margin:20px 0 36px;
}
.intent-detail .scouting-grid:has(.scouting-card:nth-child(2):last-child){
  grid-template-columns:repeat(2,minmax(0,1fr));
}
.intent-detail .scouting-card{
  padding:22px;
  border:1px solid var(--line);
  background:rgba(255,253,248,.55);
}
.intent-detail .scouting-card>span{
  display:block;
  margin-bottom:8px;
  color:var(--blue-deep);
  font-size:9px;
  font-weight:800;
  letter-spacing:.14em;
  text-transform:uppercase;
}
.intent-detail .scouting-card h3{
  margin:0 0 10px;
  color:var(--ink);
  font-size:22px;
  line-height:1.15;
}
.intent-detail .scouting-card p{
  margin:0 0 10px!important;
  font-size:13px;
  line-height:1.62;
}
.intent-detail .scouting-card p:last-child{
  margin-bottom:0!important;
}
.intent-detail .scouting-card a{
  font-size:10px;
  font-weight:800;
  letter-spacing:.08em;
  text-transform:uppercase;
}
.intent-detail .dense-v2{
  margin-top:58px;
  padding-top:8px;
}
.intent-detail .dense-intro{
  margin:-4px 0 22px!important;
  color:#6b6d72!important;
  font-size:12px!important;
  line-height:1.6!important;
}
.intent-detail .table-wrap{
  width:100%;
  margin:20px 0 36px;
  overflow-x:auto;
  -webkit-overflow-scrolling:touch;
  border:1px solid var(--line);
  background:rgba(255,253,248,.55);
}
.intent-detail .intent-table{
  width:100%;
  min-width:660px;
  border-collapse:collapse;
  color:var(--ink-soft);
  font-size:12.5px;
  line-height:1.5;
}
.intent-detail .intent-table th{
  padding:12px 14px;
  background:var(--ink);
  color:var(--white);
  font-size:9px;
  font-weight:700;
  letter-spacing:.12em;
  text-align:left;
  text-transform:uppercase;
  vertical-align:bottom;
}
.intent-detail .intent-table td{
  padding:14px;
  border-top:1px solid var(--line);
  border-right:1px solid var(--line);
  vertical-align:top;
}
.intent-detail .intent-table td:last-child,
.intent-detail .intent-table th:last-child{
  border-right:0;
}
.intent-detail .intent-table tbody tr:first-child td{
  border-top:0;
}
.intent-detail .intent-table strong{
  color:var(--ink);
}
.intent-detail .health-grid{
  display:grid;
  grid-template-columns:repeat(3,minmax(0,1fr));
  gap:10px;
  margin:20px 0 34px;
}
.intent-detail .health-card{
  padding:20px;
  border:1px solid var(--line);
  background:rgba(23,111,131,.06);
}
.intent-detail .health-card b{
  display:block;
  margin-bottom:8px;
  color:var(--ink);
  font-family:var(--serif);
  font-size:18px;
  font-weight:500;
  line-height:1.2;
}
.intent-detail .health-card span{
  display:block;
  font-size:12px;
  line-height:1.55;
}
.intent-detail .intent-faq{
  margin:58px 0 10px;
  padding-top:28px;
  border-top:1px solid var(--line);
}
.intent-detail .intent-faq h2{
  margin-top:0;
}
.intent-detail .intent-faq details{
  border-top:1px solid var(--line);
}
.intent-detail .intent-faq details:last-child{
  border-bottom:1px solid var(--line);
}
.intent-detail .intent-faq summary{
  position:relative;
  padding:17px 34px 17px 0;
  color:var(--ink);
  cursor:pointer;
  font-family:var(--serif);
  font-size:18px;
  font-weight:500;
  line-height:1.35;
  list-style:none;
}
.intent-detail .intent-faq summary::-webkit-details-marker{
  display:none;
}
.intent-detail .intent-faq summary::after{
  content:"+";
  position:absolute;
  top:15px;
  right:2px;
  color:var(--blue-deep);
  font-family:var(--sans);
  font-size:20px;
  font-weight:400;
}
.intent-detail .intent-faq details[open] summary::after{
  content:"–";
}
.intent-detail .intent-faq details p{
  margin:0 0 18px!important;
  max-width:690px;
  color:var(--ink-soft)!important;
  font-size:14px;
  line-height:1.68;
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
  .intent-detail .scouting-grid,
  .intent-detail .scouting-grid:has(.scouting-card:nth-child(2):last-child){
    grid-template-columns:1fr;
    gap:8px;
  }
  .intent-detail .trend-2026{
    margin-top:48px;
    padding-top:28px;
  }
  .intent-detail .trend-alert{
    padding:20px;
  }
  .intent-detail .health-grid{
    grid-template-columns:1fr;
    gap:8px;
  }
  .intent-detail .table-wrap{
    margin-left:calc(-1 * var(--gutter));
    width:calc(100% + 2 * var(--gutter));
    border-left:0;
    border-right:0;
  }
  .intent-detail .intent-table{
    min-width:620px;
  }
  .intent-detail .intent-faq{
    margin-top:46px;
  }
  .intent-detail .intent-faq summary{
    font-size:17px;
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
