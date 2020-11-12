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
        var margins={
            left:20,
            right:20,
            top:10,
            bottom:10
        }
        var svgH=900
        var svgW=600
        var svg=d3.select('#chart').append('svg')
            .attr('width',svgW)
            .attr('height',svgH)
        var chartW=svgW-margins.left-margins.right;
        var chartH=svgW-margins.top-margins.bottom;
        var chart=svg.append('g')
            .attr('transform',`translate(${margins.left},${margins.top})`)
        var timeP=d3.timeParse("%Y")
        var years_parsed=years.map(y=>timeP(String(y)))
        var xscale=d3.scaleTime()
            .domain(d3.extent(years_parsed))
            .range([0,chartW])
        var yscale=d3.scaleLinear()
            .domain(d3.extent(deaths))
            .range([chartH,0])
        var yaxis=d3.axisLeft(yscale)
        var xaxis=d3.axisBottom(xscale)
        .tickFormat(d3.timeFormat("%Y"))

        chart.append("g")
            .attr("transform", `translate(0, ${chartH})`)
            .call(xaxis);
        chart.append("g")
            .call(yaxis);

})})
