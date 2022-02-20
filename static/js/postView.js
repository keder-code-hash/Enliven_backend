window.onload=()=>
{
    // fix the social div after scrolling
    
    

    // load the icon for social icon
    feather.replace();

    //implementing the star rating system
    const sr=document.getElementById("starrating");
    

    for(var i=0;i<5;i++){

        const span=document.createElement('span');
        span.setAttribute("id",'starSpan '+i);
        span.setAttribute('class','fa fa-star notclicked hov');
        span.setAttribute('type','button');
        span.setAttribute('onclick','giveStar(this)');
        span.style.fontSize="30px";
        sr.append(span);
    }
    if (starCount>0){
        const starNode=document.getElementById(`starSpan ${starCount-1}`);
        giveStar(starNode);
    } 
    // main postveiw code
    const postBody=document.getElementById("postBody");
    let body=JSON.parse(postData);
    // console.log("length of the block is: ",JSON.parse(body.body_custom).blocks);
    let blocks=JSON.parse(body.body_custom).blocks;
    console.log(blocks);
    for(let ind=0;ind<=blocks.length;ind++){
        switch (blocks[ind].type) {
            case "paragraph":
                const par = document.createElement("p");
                par.innerHTML = blocks[ind].data.text;
                par.id="editorP"
                postBody.appendChild(par)
                break;
            case "Math":
                const mathSpan=document.createElement("span");
                mathSpan.className="math";
                mathSpan.innerHTML=blocks[ind].data.text;
                postBody.appendChild(mathDiv);
                break;
            case "header":
                let size=blocks[ind].data.level;
                let text=blocks[ind].data.text;
                const headerTag="h"+size;
                let header=document.createElement(headerTag);
                header.innerHTML=text;
                postBody.appendChild(header);
                break;
            case "image":
                let div=document.createElement("div");
                let img=document.createElement("img");
                let cap=document.createElement("lead");
                img.src=`${blocks[ind].data.file.url}` ;
                img.style="margin-top:10%";
                img.height=300;
                img.style="width:100%;max-width:70%;border-radius:7px;box-shadow: 10px -9px;"  
                cap.textContent=blocks[ind].data.caption;
                cap.style="margin-top:2%;font-weight:500px;margin-bottom:2%;";
                div.appendChild(img);
                div.appendChild(cap)
                div.style="width:100%;display:grid;place-items:center;padding-top:10%;padding-bottom:10%";
                postBody.appendChild(div);
                break;
            case "quote":
                let figureDiv=document.createElement("div");
                let quote=document.createElement("blockquote");
                let figCaption=document.createElement("figcaption");
                quote.innerHTML=blocks[ind].data.text
                let dash='&mdash;'
                let figVal=dash+blocks[ind].data.caption
                figCaption.innerHTML=figVal
                figureDiv.style="margin-top:15px;" +
                    "margin: 0;background: #eee;padding: 1em;" +
                    "border-radius: 1em;"
                figureDiv.appendChild(quote)
                figureDiv.appendChild(figCaption)
                postBody.appendChild(figureDiv)
                break;
            // case "raw":
            //     let blockquote = document.createElement("blockquote");
            //     let code = document.createElement("code");
            //     let pre = document.createElement("pre");
            //     pre.textContent = blocks[ind].data.html;
            //     pre.style.background = "#131313";
            //     pre.style.color = "#dddddd";
            //     pre.style.padding = "15px";
            //     code.appendChild(pre);
            //     postBody.appendChild(code);
            //     break;
            case "raw":
                let bq = document.createElement("div");
                let cd = document.createElement("code");
                let pr = document.createElement("pre");
                cd.innerText=blocks[ind].data.html; 
                // console.log(blocks[ind].data.code);
                pr.appendChild(cd); 
                bq.appendChild(pr);
                postBody.appendChild(bq);
                break;
            case "list":
                if(blocks[ind].data.style==="unordered")
                {
                    let List=document.createElement("ul");
                    for(let j=0;j<blocks[ind].data.items.length;j++)
                    {
                        let data=blocks[ind].data.items[j];
                        let ldiv=document.createElement("li");
                        ldiv.innerHTML=data;
                        List.appendChild(ldiv);
                    }
                    postBody.appendChild(List);
                }
                if(blocks[ind].data.style==="ordered")
                {
                    let List=document.createElement("ol");
                    for(let j=0;j<blocks[ind].data.items.length;j++)
                    {
                        let data=blocks[ind].data.items[j];
                        let ldiv=document.createElement("li");
                        ldiv.innerHTML=data;
                        List.appendChild(ldiv);
                    }
                    postBody.appendChild(List);
                }
                break;
            case "checklist":
                var totList=blocks[ind].data.items.length;
                for(var j=0;j<totList;j++)
                {
                    var x = document.createElement("DIV");
                    var inp=document.createElement("INPUT");                                                             
                    inp.setAttribute("type","checkbox");
                    inp.setAttribute("id","val");
                    inp.setAttribute("val","val");
                    inp.setAttribute("checked","false");
                    console.log(blocks[ind].data.items[j].checked);
                    var data=blocks[ind].data.items[j].text;
                    var t = document.createTextNode(data);
                    var lev=document.createElement("LABEL");
                    lev.setAttribute("for","val");
                    lev.appendChild(t);
                    x.append(inp,lev);
                    postBody.appendChild(x);
                }
                break;
            case "table":
                let Div=document.createElement("div");
                Div.style.marginTop='40px';
                let tableDiv=document.createElement("table")
                tableDiv.style.fontFamily='arial,sans-serif'
                tableDiv.style.borderCollapse='collapse'
                tableDiv.style.width='70%'
                tableDiv.style.border='1px solid #090909'
                tableDiv.style.padding='20px'
                tableDiv.style.margin='auto'
                let st='border: 1px solid #dddddd; text-align: left;padding: 8px;'
                let rowNo=blocks[ind].data.content.length;
                let columNo=blocks[ind].data.content[0].length;
                for (let i=0;i<rowNo;i++){
                    let tableRow=document.createElement("tr");
                    if(i===0){
                        for(let j=0;j<columNo;j++){
                            let tableHeader=document.createElement("th");
                            tableHeader.style=st;
                            let row=blocks[ind].data.content[i];
                            let tabData=row[j]
                            tableHeader.innerHTML=tabData;
                            tableRow.appendChild(tableHeader);
                        }
                    }
                    else{
                        for(let j=0;j<columNo;j++){
                            let tableData=document.createElement("td");
                            tableData.style=st;
                            let row=blocks[ind].data.content[i];
                            let tabData=row[j]
                            tableData.innerHTML=tabData;
                            tableRow.appendChild(tableData);
                        }
                    }
                tableDiv.appendChild(tableRow);
                }
                Div.appendChild(tableDiv)
                postBody.appendChild(Div)
                break;
            case "delimiter":
                let starSvg='<svg version="1.0" xmlns="http://www.w3.org/2000/svg"\n' +
                    ' width="12pt" height="12pt" viewBox="0 0 1278.000000 1280.000000"\n' +
                    ' preserveAspectRatio="xMidYMid meet">\n' +
                    '<g transform="translate(0.000000,1280.000000) scale(0.100000,-0.100000)"\n' +
                    'fill="#000000" stroke="none">\n' +
                    '<path d="M6760 12443 c-137 -26 -302 -163 -453 -375 -207 -293 -384 -645 -802\n' +
                    '-1598 -347 -790 -486 -1070 -667 -1337 -211 -311 -357 -373 -878 -374 -303 0\n' +
                    '-573 22 -1315 106 -310 36 -666 73 -930 97 -191 17 -792 17 -905 0 -359 -56\n' +
                    '-525 -174 -538 -382 -7 -128 43 -265 161 -442 197 -294 514 -612 1317 -1323\n' +
                    '955 -845 1247 -1174 1290 -1452 37 -234 -95 -656 -453 -1458 -364 -816 -430\n' +
                    '-963 -490 -1110 -252 -611 -352 -998 -318 -1236 31 -222 145 -333 357 -346\n' +
                    '311 -21 768 169 1699 704 749 431 885 508 1051 596 451 240 718 338 924 341\n' +
                    '121 1 161 -10 310 -84 265 -133 574 -380 1300 -1040 1006 -916 1405 -1206\n' +
                    '1752 -1276 102 -21 173 -13 255 27 103 50 160 135 204 304 21 81 23 111 23\n' +
                    '315 0 125 -5 267 -12 320 -51 379 -107 674 -253 1335 -229 1034 -279 1327\n' +
                    '-279 1647 0 162 16 260 55 346 101 221 462 490 1275 952 661 375 831 473 1005\n' +
                    '578 739 446 1065 761 1065 1027 0 155 -96 273 -306 378 -300 150 -748 236\n' +
                    '-1764 342 -1052 108 -1334 148 -1637 225 -387 100 -514 201 -648 515 -117 276\n' +
                    '-211 629 -391 1482 -135 644 -212 973 -289 1237 -115 398 -240 668 -380 824\n' +
                    '-94 105 -221 156 -335 135z"/>\n' +
                    '</g>\n' +
                    '</svg>\n'
                let deliDiv=document.createElement("div");
                deliDiv.className='container-fluid';
                deliDiv.style='display: flex;\n' +
                    '  justify-content: center;'
                let sectionDiv=document.createElement("h2");
                let pDiv=document.createElement("p");
                pDiv.style='justify-content: center;'
                pDiv.innerHTML=starSvg+starSvg+starSvg;
                sectionDiv.appendChild(pDiv);
                deliDiv.appendChild(sectionDiv)
                postBody.appendChild(deliDiv)
                break;
            default:
                break;
        }
    }
    renderMathInElement(document.body, { 
        delimiters: [
              {left: '$$', right: '$$', display: true},
              {left: '$', right: '$', display: false},
              {left: '\\(', right: '\\)', display: false},
              {left: '\\[', right: '\\]', display: true}, 
              {left: "\\(", right: "\\)", display: false},
              {left: "\\begin{equation}", right: "\\end{equation}", display: true},
              {left: "\\begin{align}", right: "\\end{align}", display: true},
              {left: "\\begin{alignat}", right: "\\end{alignat}", display: true},
              {left: "\\begin{gather}", right: "\\end{gather}", display: true},
              {left: "\\begin{CD}", right: "\\end{CD}", display: true},
              {left: "\\[", right: "\\]", display: true}
        ], 
        throwOnError : false
      });
      var math = document.getElementsByClassName('math');
      for (var i = 0; i < math.length; i++) {
          katex.render(math[i].textContent, math[i]);
      } 
};