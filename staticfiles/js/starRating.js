var prevClicked=-1;

function Rate(className,color,ncEv,cEv){
    className.style.color=color;
    className.classList.toggle("notclicked",ncEv);
    className.classList.toggle("clicked",cEv);
}

function giveStar(clickedNode){
    const parentNode=clickedNode.parentNode;
    var starBt=parentNode.childNodes;
     
    // console.log(starBt)
    var currentNodeId=parseInt(clickedNode.id.split(' ')[1]);
    
    
    if(clickedNode.classList.contains("notclicked") && currentNodeId>prevClicked){
        for(var currentIndex=0;currentIndex<5;currentIndex++){
            if(currentIndex<=currentNodeId){
                Rate(starBt[currentIndex],"orange",false,true);
                }
        }
        prevClicked=currentNodeId;
    }
    else if(clickedNode.classList.contains("clicked") && currentNodeId<prevClicked)
    {
        for(var currentIndex=currentNodeId+1;currentIndex<=prevClicked;currentIndex++){
            Rate(starBt[currentIndex],"black",true,false);
        }
        prevClicked=currentNodeId;
    }
    else if(currentNodeId==prevClicked && clickedNode.classList.contains("clicked")){
        for(var currentIndex=0;currentIndex<=currentNodeId;currentIndex++){
            Rate(starBt[currentIndex],"black",true,false);
        }
        prevClicked=-1;
    }
    
    var rateValue= (prevClicked==-1) ? 0 : (currentNodeId+1);
    // document.getElementById('ratVal').innerHTML=rateValue;
    // document.getElementById('ratVal').setAttribute('value',rate);

    sendData(rateValue);

}

