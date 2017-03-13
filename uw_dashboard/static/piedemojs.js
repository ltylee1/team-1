google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawFundingStreamChart);

// data = [['category1': 3], ['category2': 2]]
function graphInstance(data){
    return google.visualization.arrayToDataTable(data)
}

function draw(id, title, graphData){
    var options = {
        title: title
    };

    var chart = new google.visualization.PieChart(document.getElementById(id));
    chart.draw(graphData, options);
}

function drawFundingStreamChart() {
    var id = "funding_stream";
    var title = "Funding Stream";
    var rawData = {};

    {% for data in results %}
        rawData[data.funding_stream] = data.allocation
    {% endfor %}

    var graphData = graphInstance(rawData);
    draw(id, title, graphData)
}





//    <div id="funding_stream" class="graph"></div>
//    <div id="donor_engagement" class="graph"></div>
//    <div id="year" class="graph"></div>
//    <div id="program_planner" class="graph"></div>
//    <div id="element_name" class="graph"></div>
//    <div id="city" class="graph"></div>
//    <div id="specific_element" class="graph"></div>
//    <div id="strategic_outcome" class="graph"></div>
//    <div id="city_grouping" class="graph"></div>
//    <div id="level_name" class="graph"></div>
//    <div id="target_population" class="graph"></div>
//    <div id="focus_area" class="graph"></div>