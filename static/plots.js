// plots
$(document).ready(function (){
    d3.json('http://127.0.0.1:5000/api_v1/Wide_agg').then(function(data){
        var org_data=[]
        var temp=data.map(obj=>obj.State)
        var deaths=data.map(obj=>obj.Deaths)
        var years=[2011,2012,2013,2014,2015,2016,2017]
        var states = [];
        temp.forEach((c) => {  
        if (!states.includes(c)) {
            states.push(c);
            }
        });
        console.log(states)
        var i=0
        var j=0
        var arr=[]
        var obj={}
        var valid=0
        console.log(deaths.length)
        deaths.forEach(function(d){
            var check=i%7
            if (check==0 && valid==1||i==349){
                if(i==349){
                    arr.push(d)
                }
                obj[states[j]]=arr
                org_data.push(obj)
                arr=[]
                obj={}
                j=j+1
            }
            valid=1
            i=i+1
            arr.push(d)
        })
        console.log(org_data)
        
})})
