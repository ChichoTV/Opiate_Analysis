// plots
console.log('hello')


d3.json('http://127.0.0.1:5000/api_v1/Wide_agg').then(function(data){
    Object.values(data).forEach(function(d){
        console.log(d)
    })
})