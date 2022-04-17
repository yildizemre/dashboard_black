import json



with open('./static/assets/json_files/MOCK_DATA (2).json') as json_file:
    data = json.load(json_file)
#     print(data['module_list'])

import pandas as pd
dataframe = pd.DataFrame.from_dict(data)
dataframe=dataframe.dropna()
# print(dataframe)
dataframe=dataframe.reset_index()
#gün bazlı
for i in range(len(dataframe)):
    (dataframe['date'].loc[i])=(dataframe['date'].loc[i])[0:10]
    # dataframe['date']=dataframe['date'][0:15]

# dataframe=dataframe.drop_duplicates(subset=['date'])

line_dataframe=dataframe.sort_values(by='date', ascending=False)
el=(line_dataframe['date'].value_counts())
df = el.to_frame()
df=df.reset_index()
df=df.sort_values(by='index', ascending=False)
df=df.reset_index()
# print(df)
line_index_array = []
line_value_array = []
print("lllineee")
print(df)
df=df[:30]
for i in range(len(df)):
  line_index_array.append(df['index'].iloc[i])
  line_value_array.append(df['date'].iloc[i])
#gün bazlı


#box chart
for i in range(len(dataframe)):
    (dataframe['date'].loc[i])=(dataframe['date'].loc[i])[0:7]

box_dataframe=dataframe.sort_values(by='date', ascending=False)
box=(box_dataframe['date'].value_counts())
df_box = box.to_frame()
df_box=df_box.reset_index()
df_box=df_box.sort_values(by='index', ascending=False)
df_box=df_box.reset_index()
df_box=(df_box[0:12])
dfbox_index_array = []
dfbox_value_array = []
print("boxxx")
print(df_box)
for i in range(len(df_box)):
  dfbox_index_array.append(df_box['index'].iloc[i])
  dfbox_value_array.append(df_box['date'].iloc[i])
  





#box chart


#area chart

area_dataframe=dataframe.sort_values(by='cam_no', ascending=False)
area_dataframe=(area_dataframe['cam_no'].value_counts())

area_dataframe = area_dataframe.to_frame()
area_dataframe=area_dataframe.reset_index()
area_dataframe=area_dataframe.sort_values(by='index', ascending=False)
area_dataframe=area_dataframe.reset_index()
area_index_array = []
area_value_array = []
print("area")
print(area_dataframe)
for i in range(len(area_dataframe)):
  area_index_array.append(area_dataframe['index'].iloc[i])
  area_value_array.append(area_dataframe['cam_no'].iloc[i])
#areachart



#Doughnut Chart

doughnut_dataframe=dataframe.sort_values(by='name', ascending=False)
doughnut_dataframe=(doughnut_dataframe['name'].value_counts())
doughnut_dataframe = doughnut_dataframe.to_frame()
doughnut_dataframe=doughnut_dataframe.reset_index()
doughnut_dataframe=doughnut_dataframe.sort_values(by='index', ascending=False)
doughnut_dataframe=doughnut_dataframe.reset_index()

print(doughnut_dataframe)
doughnut_index_array = []
doughnut_value_array = []
for i in range(len(doughnut_dataframe)):
  doughnut_index_array.append(doughnut_dataframe['index'].iloc[i])
  doughnut_value_array.append(doughnut_dataframe['name'].iloc[i])


#Doughnut Chart


with open("./static/assets/js/chart.js", 'w') as file:
    file.write("""
$(function() {
  /* ChartJS
   * -------
   * Data and config for chartjs
   */
  'use strict';
  var data = {
    labels: """+str(line_index_array)+""",
    datasets: [{
      label: '# of Votes',
      data: """+str(line_value_array)+""",
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)',
      ],
      borderColor: [
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)',
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)',
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)',
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)',
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)',
        
      ],
      borderWidth: 1,
      fill: false
    }]
  };
var data_bar = {
    labels: """+str(dfbox_index_array)+""",
    datasets: [{
      label: '# of Votes',
      data: """+str(dfbox_value_array) +""",
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)'
      ],
      borderColor: [
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)',
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)',
        
      ],
      borderWidth: 1,
      fill: false
    }]
  };

  var options = {
    scales: {
      yAxes: [{
        ticks: {
          beginAtZero: true
        },
        gridLines: {
          color: "rgba(204, 204, 204,0.1)"
        }
      }],
      xAxes: [{
        gridLines: {
          color: "rgba(204, 204, 204,0.1)"
        }
      }]
    },
    legend: {
      display: false
    },
    elements: {
      point: {
        radius: 0
      }
    }
  };
var doughnutPieData = {
    datasets: [{
      data: """+str(doughnut_value_array)+""",
      backgroundColor: [
        'rgba(255, 99, 132, 0.5)',
        'rgba(54, 162, 235, 0.5)',
        'rgba(255, 206, 86, 0.5)',
        'rgba(75, 192, 192, 0.5)',
        'rgba(153, 102, 255, 0.5)',
        'rgba(255, 159, 64, 0.5)'
      ],
      borderColor: [
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)'
      ],
    }],

    // These labels appear in the legend and in the tooltips when hovering different arcs
    labels: """+str(doughnut_index_array)+"""
  };

  var doughnutPieOptions = {
    responsive: true,
    animation: {
      animateScale: true,
      animateRotate: true
    }
  };

  var areaData = {
    labels: """+str(area_index_array)+""",
    datasets: [{
      label: '# of Votes',
      data: """+str(area_value_array)+""",
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)'
      ],
      borderColor: [
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)'
      ],
      borderWidth: 1,
      fill: true, // 3: no fill
    }]
  };

  var areaOptions = {
    plugins: {
      filler: {
        propagate: true
      }
    },
    scales: {
      yAxes: [{
        gridLines: {
          color: "rgba(204, 204, 204,0.1)"
        }
      }],
      xAxes: [{
        gridLines: {
          color: "rgba(204, 204, 204,0.1)"
        }
      }]
    }
  }

  // Get context with jQuery - using jQuery's .get() method.
  if ($("#barChart").length) {
    var barChartCanvas = $("#barChart").get(0).getContext("2d");
    // This will get the first returned node in the jQuery collection.
    var barChart = new Chart(barChartCanvas, {
      type: 'bar',
      data: data_bar,
      options: options
    });
  }

  if ($("#lineChart").length) {
    var lineChartCanvas = $("#lineChart").get(0).getContext("2d");
    var lineChart = new Chart(lineChartCanvas, {
      type: 'line',
      data: data,
      options: options
    });
  }

 


  if ($("#doughnutChart").length) {
    var doughnutChartCanvas = $("#doughnutChart").get(0).getContext("2d");
    var doughnutChart = new Chart(doughnutChartCanvas, {
      type: 'doughnut',
      data: doughnutPieData,
      options: doughnutPieOptions
    });
  }

  

  if ($("#areaChart").length) {
    var areaChartCanvas = $("#areaChart").get(0).getContext("2d");
    var areaChart = new Chart(areaChartCanvas, {
      type: 'line',
      data: areaData,
      options: areaOptions
    });
  }

  
});
""".strip())