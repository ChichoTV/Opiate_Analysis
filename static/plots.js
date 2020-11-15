// plots
$(document).ready(function (){
    d3.json('http://127.0.0.1:5000/api_v1/Wide_agg').then(function(data){
        var org_data=[]
        var temp=data.map(obj=>obj.State)
        var deaths=data.map(obj=>obj.Deaths)
        var years=['2011','2012','2013','2014','2015','2016','2017']
        var states = [];
        temp.forEach((c) => {  
        if (!states.includes(c)) {
            states.push(c);
            }
        });
        // console.log(states)
        var i=0
        var j=0
        var arr=[]
        var obj={}
        var valid=0
        deaths.forEach(function(d){
            var check=i%7
            if (check==0 && valid==1||i==349){
                if(i==349){
                    arr.push(d)
                }
                obj[states[j]]=arr
                org_data.push(obj)
                arr=[]
                j=j+1
            }
            valid=1
            i=i+1
            arr.push(d)
        })
        var timeP=d3.timeParse("%Y");
        var years_parsed=years.map(y=>timeP(String(y)));
        console.log(obj);

        var inp_states=d3.select('#state1');
        var form=d3.select('form');
        var button=d3.select('#filter-btn1');
        // plot functions
        function init(){
        var trace={
            y:org_data[1].Alaska,
            x:years,
            type:'line',
            name:"Alaska"
        }
        var data=[trace]
        var layout={
            title:'Opioid Deaths By State'
        }
        Plotly.newPlot('plot1',data,layout)
    }   

        // plot updater functions
        function update1(){
            d3.event.preventDefault();
            var inpv_states=inp_states.property('value');
            console.log(inpv_states)
            var inp_array=inpv_states.split(',')
            // console.log(inp_array)
            var data1=[]
            inp_array.forEach(function(d){
                trace1={
                    x:years,
                    y:obj[d],
                    type:'line',
                    name: d
                }
                data1.push(trace1);

            })
            layout={
                title:'Opioid Deaths By State'
            }

            Plotly.newPlot('plot1',data1,layout);
        }
        // var margins={
        //     left:40,
        //     right:20,
        //     top:10,
        //     bottom:10
        // }
        // var svgH=900
        // var svgW=700
        // var svg=d3.select('#chart').append('svg')
        //     .attr('width',svgW)
        //     .attr('height',svgH)
        // var chartW=svgW-margins.left-margins.right;
        // var chartH=svgW-margins.top-margins.bottom;
        // var chart=svg.append('g')
        //     .attr('transform',`translate(${margins.left},${margins.top})`)
        // var timeP=d3.timeParse("%Y")
        // var years_parsed=years.map(y=>timeP(String(y)))
        // var xscale=d3.scaleTime()
        //     .domain(d3.extent(years_parsed))
        //     .range([0,chartW])
        // var yscale=d3.scaleLinear()
        //     .domain(d3.extent(deaths))
        //     .range([chartH,0])
        // var yaxis=d3.axisLeft(yscale)
        // var xaxis=d3.axisBottom(xscale)
        // .tickFormat(d3.timeFormat("%Y"))
        // chart.append("g")
        //     .attr("transform", `translate(0, ${chartH})`)
        //     .call(xaxis);
        // chart.append("g")
        //     .call(yaxis);
        // chart.append('path')
        //     .data(org_data[16].Kentucky)
        //     .attr('fill', 'red')
        //     .attr('stroke','steelblue')
        //     .attr('stroke-width',1.5)
        //     .attr('d',d3.line([[timeP(2011) ,150],[timeP(2012),600],[timeP(2013),100]])
        //     .x(function(d,i) {return xscale(years_parsed[i])})
        //     .y(function (d) {return yscale(d)}))
        // console.log(org_data[16])
        // var temp=[200,1200,600,1800]
        // var myline=d3.line()
        //     .x(function(d,i){return xscale(years_parsed[i])})
        //     .y(d=>yscale(d))
        // var lines=chart.selectAll('path')
        //     .data(temp)
        //     .append('path')
        //     .attr('d', myline)
        init();
        button.on('click',update1);
        form.on('submit',update1);

})
d3.json('http://127.0.0.1:5000/api_v1/percents').then(function(data){
    var inp_states=d3.select('#state2');
    var form=d3.select('form');
    var button=d3.select('#filter-btn2');
    console.log(data)
    trace={
        x:Object.keys(data),
        y:Object.values(data),
        type:'bar',
        name:'bar'
    }
    layout={
        title:"Opioid Deaths Per 100,000 People (2014)"
    }
    Plotly.newPlot('plot2',[trace],layout)
    function update2(){
        d3.event.preventDefault();
        var inpv_states=inp_states.property('value');
        // console.log(inpv_states)
        var inp_array=inpv_states.split(',')
        var data2=[]
        inp_array.forEach(function (d){
            trace2={
                x:[d],
                y:[data[d]],
                type:'bar',
                name:d
            }
            data2.push(trace2);
        })
        layout={
            title:"Opioid Deaths Per 100,000 People (2014)"
        }
        Plotly.newPlot('plot2',data2,layout)
    }

    button.on('click',update2);
    form.on('submit',update2);
})
})


