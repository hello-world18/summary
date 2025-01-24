
          // Tab Navigation
          const tabButtons = document.querySelectorAll(".tab-button");
          const departments = document.querySelectorAll(".department-section");
          document.getElementById('print-button').addEventListener('click', () => {
            window.print();
          });
         
        //opd download
          document.getElementById('opdDownload').addEventListener('click', async () => {
            const { jsPDF } = window.jspdf;
        
            const pdf = new jsPDF('p', 'mm', 'a4'); // Create jsPDF instance
            const options = { scale: 2 }; // Higher scale improves quality
        
            let deptCanvas, categoryCanvas, opdVisCanvas, opdCatVisCanvas;
            try {
                // Capture department and category summaries
                deptCanvas = await html2canvas(document.querySelector('.opdContainer'), options);
                categoryCanvas = await html2canvas(document.querySelector('.opdCategoryContainer'), options);
        
                // Capture visualizations
                opdVisCanvas = await html2canvas(document.getElementById('deptChart'), options);
                opdCatVisCanvas = await html2canvas(document.getElementById('categoryChart'), options);
            } catch (error) {
                console.error("Error capturing canvas: ", error);
                return;
            }
        
            // Validate captured canvases
            if (!deptCanvas || !categoryCanvas || !opdVisCanvas || !opdCatVisCanvas) {
                console.error("One or more canvases failed to render");
                return;
            }
        
            const pageWidth = pdf.internal.pageSize.getWidth();
            const imgWidth = pageWidth - 20;
            
            try {
                const deptImgHeight = (deptCanvas.height / deptCanvas.width) * imgWidth;
                pdf.text('OPD Department Wise Summary', 10, 10);
                pdf.addImage(deptCanvas.toDataURL('image/png'), 'PNG', 10, 20, imgWidth, deptImgHeight);
        
                pdf.addPage();
                const deptVisImgHeight = (opdVisCanvas.height / opdVisCanvas.width) * imgWidth;
                pdf.text('OPD Department Visualization', 10, 10);
                pdf.addImage(opdVisCanvas.toDataURL('image/png'), 'PNG', 10, 20, imgWidth, deptVisImgHeight);

                pdf.addPage();
                const categoryImgHeight = (categoryCanvas.height / categoryCanvas.width) * imgWidth;
                pdf.text('OPD Category Wise Summary', 10, 10);
                pdf.addImage(categoryCanvas.toDataURL('image/png'), 'PNG', 10, 20, imgWidth, categoryImgHeight);
        
                
        
                pdf.addPage();
                const categoryVisImgHeight = (opdCatVisCanvas.height / opdCatVisCanvas.width) * imgWidth;
                pdf.text('OPD Category Visualization', 10, 10);
                pdf.addImage(opdCatVisCanvas.toDataURL('image/png'), 'PNG', 10, 20, imgWidth, categoryVisImgHeight);
        
                pdf.save('OPD-summary.pdf');
            } catch (error) {
                console.error("Error adding image to PDF: ", error);
            }
        });
        //ipd download
        document.getElementById('ipdDownload').addEventListener('click', async () => {
          const { jsPDF } = window.jspdf;
          const pdf = new jsPDF('p', 'mm', 'a4'); // Create jsPDF instance
          const options = { scale: 2, useCORS: true, willReadFrequently: true };
      
          let ipdDeptCanvas, ipdVisCanvas;
          try {
              // Capture department and visualization sections
              const deptContainer = document.querySelector('.ipdContainer');
              const visDiv = document.querySelector('.vis-div'); 
              ipdDeptCanvas = await html2canvas(deptContainer, options);
              ipdVisCanvas = await html2canvas(visDiv, options);
              
          } catch (error) {
              console.error("Error capturing canvas: ", error);
              return;
          }
      
          if (!ipdDeptCanvas || !ipdVisCanvas) {
              console.error("One or more canvases failed to render");
              return;
          }
      
          const pageWidth = pdf.internal.pageSize.getWidth();
          const imgWidth = pageWidth - 20;
      
          try {
              const deptImgHeight = (ipdDeptCanvas.height / ipdDeptCanvas.width) * imgWidth;
              pdf.text('IPD Department Wise Summary', 10, 10);
              pdf.addImage(ipdDeptCanvas.toDataURL('image/png'), 'PNG', 10, 20, imgWidth, deptImgHeight);
      
              pdf.addPage();
              const deptVisImgHeight = (ipdVisCanvas.height / ipdVisCanvas.width) * imgWidth;
              pdf.text('IPD Department Visualization', 10, 10);
              pdf.addImage(ipdVisCanvas.toDataURL('image/png'), 'PNG', 10, 20, imgWidth, deptVisImgHeight);
      
              pdf.save('IPD-summary.pdf');
          } catch (error) {
              console.error("Error adding image to PDF: ", error);
          }
      });
      //Doctors download
      document.getElementById('doctorDownload').addEventListener('click', async () => {
        const { jsPDF } = window.jspdf;
          const pdf = new jsPDF('p', 'mm', 'a4');
        const deptContainer = document.querySelector('.doctor-section');
        const originalStyles = deptContainer.style.cssText;
        
        // Temporarily override styles
        deptContainer.style.animation = 'none';
        deptContainer.style.transform = 'none';
        
        const options = { scale: 2, useCORS: true, backgroundColor: null };
        
        try {
            drDeptCanvas = await html2canvas(deptContainer, options);
        } catch (error) {
            console.error("Error capturing canvas: ", error);
        }
        
        // Restore original styles
        deptContainer.style.cssText = originalStyles;
        
        // Save to PDF
        if (drDeptCanvas) {
            const pdf = new jsPDF('p', 'mm', 'a4');
            const pageWidth = pdf.internal.pageSize.getWidth();
            const imgWidth = pageWidth - 20;
            const imgHeight = (drDeptCanvas.height / drDeptCanvas.width) * imgWidth;
        
            
            pdf.addImage(drDeptCanvas.toDataURL('image/png'), 'PNG', 10, 20, imgWidth, imgHeight);
            pdf.save('Doctor-summary.pdf');
        }
        
      });
      document.getElementById('lisDownload').addEventListener('click', async () => {
        const { jsPDF } = window.jspdf;
    
        const pdf = new jsPDF('p', 'mm', 'a4'); // Create jsPDF instance
        const options = { scale: 2 }; // Higher scale improves quality
    
        let lisDataCanvas, lisOpCanvas, lisIpCanvas, lisCategoryCanvas, lisCategoryVisCanvas;
    
        try {
            // Capture different sections as canvases
            lisDataCanvas = await html2canvas(document.querySelector('.lis-container'), options);
            lisOpCanvas = await html2canvas(document.querySelector('.lisOp'), options);
            lisIpCanvas = await html2canvas(document.querySelector('.lisIp'), options);
            lisCategoryCanvas = await html2canvas(document.querySelector('.lis-category-container'), options);
            lisCategoryVisCanvas = await html2canvas(document.querySelector('.lis-category-vis'), options);
        } catch (error) {
            console.error("Error capturing canvas: ", error);
            return;
        }
    
        // Validate captured canvases
        if (!lisDataCanvas || !lisOpCanvas || !lisIpCanvas || !lisCategoryCanvas || !lisCategoryVisCanvas) {
            console.error("One or more canvases failed to render");
            return;
        }
    
        const pageWidth = pdf.internal.pageSize.getWidth();
        const imgWidth = pageWidth - 20;
    
        try {
            // Add LIS Data Summary
            const lisDataImgHeight = (lisDataCanvas.height / lisDataCanvas.width) * imgWidth;
            pdf.text('LIS Data Summary', 10, 10);
            pdf.addImage(lisDataCanvas.toDataURL('image/png'), 'PNG', 10, 20, imgWidth, lisDataImgHeight);
    
            // Add LIS OP Summary
            pdf.addPage();
            const lisOpImgHeight = (lisOpCanvas.height / lisOpCanvas.width) * imgWidth;
            pdf.text('LIS OP Summary', 10, 10);
            pdf.addImage(lisOpCanvas.toDataURL('image/png'), 'PNG', 10, 20, imgWidth, lisOpImgHeight);
    
            // Add LIS IP Summary
            pdf.addPage();
            const lisIpImgHeight = (lisIpCanvas.height / lisIpCanvas.width) * imgWidth;
            pdf.text('LIS IP Summary', 10, 10);
            pdf.addImage(lisIpCanvas.toDataURL('image/png'), 'PNG', 10, 20, imgWidth, lisIpImgHeight);
    
            // Add LIS Category Summary
            pdf.addPage();
            const lisCategoryImgHeight = (lisCategoryCanvas.height / lisCategoryCanvas.width) * imgWidth;
            pdf.text('LIS Category Summary', 10, 10);
            pdf.addImage(lisCategoryCanvas.toDataURL('image/png'), 'PNG', 10, 20, imgWidth, lisCategoryImgHeight);
    
            // Add LIS Category Visualization
            pdf.addPage();
            const lisCategoryVisImgHeight = (lisCategoryVisCanvas.height / lisCategoryVisCanvas.width) * imgWidth;
            pdf.text('LIS Category Visualization', 10, 10);
            pdf.addImage(lisCategoryVisCanvas.toDataURL('image/png'), 'PNG', 10, 20, imgWidth, lisCategoryVisImgHeight);
    
            // Save the PDF
            pdf.save('LIS-summary.pdf');
        } catch (error) {
            console.error("Error adding image to PDF: ", error);
        }
    });
    document.getElementById('otDownload').addEventListener('click', async () => {
      const { jsPDF } = window.jspdf;
  
      const pdf = new jsPDF('p', 'mm', 'a4'); // Create jsPDF instance
      const options = { scale: 2 }; // Higher scale improves quality
  
      let minorOtCanvas, minorOtChartCanvas, majorOtCanvas, majorOtChartCanvas;
  
      try {
          // Capture different sections as canvases
          minorOtCanvas = await html2canvas(document.querySelector('.minor-ot-container'), options);
          minorOtChartCanvas = await html2canvas(document.getElementById('minorOtChart'), options);
          majorOtCanvas = await html2canvas(document.querySelector('.major-ot-container'), options);
          majorOtChartCanvas = await html2canvas(document.getElementById('majorOtChart'), options);
      } catch (error) {
          console.error("Error capturing canvas: ", error);
          return;
      }
  
      // Validate captured canvases
      if (!minorOtCanvas || !minorOtChartCanvas || !majorOtCanvas || !majorOtChartCanvas) {
          console.error("One or more canvases failed to render");
          return;
      }
  
      const pageWidth = pdf.internal.pageSize.getWidth();
      const imgWidth = pageWidth - 20;
  
      try {
          // Add Minor OT Table
          const minorOtImgHeight = (minorOtCanvas.height / minorOtCanvas.width) * imgWidth;
          pdf.text('Minor OT Summary', 10, 10);
          pdf.addImage(minorOtCanvas.toDataURL('image/png'), 'PNG', 10, 20, imgWidth, minorOtImgHeight);
  
          // Add Minor OT Chart
          pdf.addPage();
          const minorOtChartImgHeight = (minorOtChartCanvas.height / minorOtChartCanvas.width) * imgWidth;
          pdf.text('Minor OT Chart', 10, 10);
          pdf.addImage(minorOtChartCanvas.toDataURL('image/png'), 'PNG', 10, 20, imgWidth, minorOtChartImgHeight);
  
          // Add Major OT Table
          pdf.addPage();
          const majorOtImgHeight = (majorOtCanvas.height / majorOtCanvas.width) * imgWidth;
          pdf.text('Major OT Summary', 10, 10);
          pdf.addImage(majorOtCanvas.toDataURL('image/png'), 'PNG', 10, 20, imgWidth, majorOtImgHeight);
  
          // Add Major OT Chart
          pdf.addPage();
          const majorOtChartImgHeight = (majorOtChartCanvas.height / majorOtChartCanvas.width) * imgWidth;
          pdf.text('Major OT Chart', 10, 10);
          pdf.addImage(majorOtChartCanvas.toDataURL('image/png'), 'PNG', 10, 20, imgWidth, majorOtChartImgHeight);
  
          // Save the PDF
          pdf.save('OT-summary.pdf');
      } catch (error) {
          console.error("Error adding image to PDF: ", error);
      }
  });
  document.getElementById('biopsyDownload').addEventListener('click', async () => {
    const { jsPDF } = window.jspdf;

    const pdf = new jsPDF('p', 'mm', 'a4'); // Create jsPDF instance
    const options = { scale: 2 }; // Higher scale improves quality

    let biopsyTableCanvas;
    try {
        // Capture biopsy table and chart as canvases
        biopsyTableCanvas = await html2canvas(document.querySelector('.biopsy-container'), options);
    } catch (error) {
        console.error("Error capturing canvas: ", error);
        return;
    }

    // Validate captured canvases
    if (!biopsyTableCanvas ) {
        console.error("One or more canvases failed to render");
        return;
    }

    const pageWidth = pdf.internal.pageSize.getWidth();
    const imgWidth = pageWidth - 20;

    try {
        // Add Biopsy Table
        const biopsyTableImgHeight = (biopsyTableCanvas.height / biopsyTableCanvas.width) * imgWidth;
        pdf.text('Biopsy Count Summary', 10, 10);
        pdf.addImage(biopsyTableCanvas.toDataURL('image/png'), 'PNG', 10, 20, imgWidth, biopsyTableImgHeight);


        // Save the PDF
        pdf.save('Biopsy-summary.pdf');
    } catch (error) {
        console.error("Error adding image to PDF: ", error);
    }
  });

          tabButtons.forEach((button, index) => {
                    button.addEventListener("click", () => {
                      // Update active tab
                      tabButtons.forEach((btn) => btn.classList.remove("active"));
                      button.classList.add("active");

                      // Show selected department
                      departments.forEach((dept, deptIndex) => {
                        if (index === deptIndex) {
                          dept.style.display = "block";
                          // Trigger animation
                          dept.style.opacity = "0";
                          dept.style.transform = "translateY(20px)";
                          setTimeout(() => {
                            dept.style.opacity = "1";
                            dept.style.transform = "translateY(0)";
                          }, 50);
                        } else {
                          dept.style.display = "none";
                        }
                      });
                    });
                  });

                  // Initialize the first tab as visible
                  departments.forEach((dept, index) => {
                    dept.style.display = index === 0 ? "block" : "none";
                  });
        
          <!--Opd charts-->
                document.getElementById('generate-dept-chart').addEventListener('click', function() {
                    

                    const labels = {{ departments_json | tojson | safe }};
                    const data = {{ daily_opd_count_json | tojson | safe }};
                    const required = {{ opd_required_json | tojson | safe }};
                    console.log(labels)
                    const deptChart = document.getElementById('deptChart');
                    new Chart(deptChart, {
                      type: 'bar',
                      data: {
                          labels: labels,
                          datasets: [
                          {
                              label: 'OPD Required',
                              data: required,
                              backgroundColor: 'rgba(75, 192, 192, 0.2)',
                              borderColor: 'rgba(75, 192, 192, 1)',
                              borderWidth: 1
                          },
                          {
                              label: 'OPD Count',
                              data: data,
                              backgroundColor: 'rgba(85, 223, 117, 0.6)',
                              borderColor: 'rgba(3, 32, 7, 0.35)',
                              borderWidth: 1
                          }
                          ]
                      },
                      options: {
                          plugins: {
                            legend: {
                              labels: {
                                  font: {
                                      size: 16, // Font size for legend
                                      weight: 'bold', // Bold legend text
                                  },
                                  color: '#333', // Color of legend text
                              }
                            },
                            datalabels: {
                              color: '#000', // Color of the data labels
                              anchor: 'end', // Positioning of the label
                              align: 'top', // Alignment of the label
                              font: {
                                  size: 14, // Font size for data labels
                                  weight: 'bold', // Bold data labels
                              },
                              formatter: function (value) {
                                  return value; // Display the value
                              }
                            }
                          },
                          scales: {
                            x: {
                            ticks: {
                                font: {
                                    size: 14, // Font size for X-axis labels
                                    weight: 'bold' // Bold X-axis labels
                                },
                                color: '#333' // Color of X-axis labels
                            }
                            },
                            y: {
                            ticks: {
                                font: {
                                    size: 14, // Font size for Y-axis labels
                                    weight: 'bold' // Bold Y-axis labels
                                },
                                color: '#333' // Color of Y-axis labels
                            },
                            beginAtZero: true
                            }
                          }
                      },
                      plugins: [ChartDataLabels] // Register the plugin
                    });
        
                  });
          <!--Opd category charts-->
                                        document.getElementById('generate-category-chart').addEventListener('click', function() {
                                            const labels = {{ categories_json | tojson | safe }};
                                            const data = {{ patient_counts_json | tojson | safe }};

                                            const categoryChart = document.getElementById('categoryChart')
                                            new Chart(categoryChart, {
                                                type: 'pie',
                                                data: {
                                                    labels: labels,
                                                    datasets: [{
                                                        data: data,
                                                        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0']
                                                    }]
                                                },options: {
                                                  responsive: false,
                                                  maintainAspectRatio: false,
                                                  plugins: {
                                                      legend: {
                                                        position: 'right',
                                                        labels: {
                                                          font: {
                                                              size: 14, // Font size for the legend
                                                              weight: 'bold', // Optional: Make the legend text bold
                                                          },
                                                          color: '#000', // Legend text color
                                                      }
                                                      },datalabels: {
                                                        color: '#000',
                                                        font: {
                                                          size: 14, // Set the font size (in pixels)
                                                          weight: 'bold', // Optional: Make the text bold
                                                      },  // Color of the text
                                                        anchor: 'top', // Positioning of the label
                                                        align: 'top', // Alignment of the label
                                                        formatter: function(value) {
                                                            return value; // Display the value
                                                        }
                                                    }
                                                  }
                                              },plugins: [ChartDataLabels]
                                            });
                                        });

          
          <!--IPD charts-->
                    
          

                                        document.getElementById('generate--chart-ipd').addEventListener('click', function () {
                                            const departmentNames = {{ department_names | tojson | safe }};
                                            const ipd80Percent = {{ ipd80Percent | tojson | safe }};
                                            const totalCounts = {{ totalCounts | tojson | safe }};
                                            const PatientGeneral = {{ PatientGeneral | tojson | safe }};
                                            const General = {{ General | tojson | safe }};
                                            const ctx = document.getElementById('ipd-chart').getContext('2d');
                                            
                                            // Create the chart using Chart.js
                                            new Chart(ctx, {
                                                type: 'bar',
                                                data: {
                                                    labels: departmentNames, // X-axis labels (Departments)
                                                    datasets: [
                                                        {
                                                            label: 'IPD 80%',
                                                            data: ipd80Percent,
                                                            backgroundColor: 'rgba(75, 192, 192, 0.6)',
                                                            borderColor: 'rgba(75, 192, 192, 1)',
                                                            borderWidth: 1,
                                                        },
                                                        {
                                                            label: 'Patient General',
                                                            data: PatientGeneral,
                                                            backgroundColor: 'rgba(255, 99, 132, 0.6)',
                                                            stack: 'TotalCount'
                                                          },
                                                          {
                                                            label: 'General+Aarogyasri+ESH',
                                                            data: General,
                                                            backgroundColor: 'rgba(255, 206, 86, 0.6)',
                                                            stack: 'TotalCount'
                                                          },

                                                        ]
                                                      },

                                                options: {
                                                  plugins: {
                                                    legend: {
                                                        labels: {
                                                            font: {
                                                                size: 16, // Font size for legend
                                                                weight: 'bold', // Bold legend text
                                                            },
                                                            color: '#333', // Color of legend text
                                                        }
                                                    },
                                                    datalabels: {
                                                        color: '#000', // Color of the data labels
                                                        anchor: 'end', // Positioning of the label
                                                        align: 'top', // Alignment of the label
                                                        font: {
                                                            size: 14, // Font size for data labels
                                                            weight: 'bold', // Bold data labels
                                                        },
                                                        formatter: function (value) {
                                                            return value; // Display the value
                                                        }
                                                    }
                                                },
                                                    scales: {
                                                      x: {
                                                          ticks: {
                                                              font: {
                                                                  size: 14, // Font size for X-axis labels
                                                                  weight: 'bold' // Bold X-axis labels
                                                              },
                                                              color: '#333' // Color of X-axis labels
                                                          }
                                                      },
                                                      y: {
                                                          ticks: {
                                                              font: {
                                                                  size: 14, // Font size for Y-axis labels
                                                                  weight: 'bold' // Bold Y-axis labels
                                                              },
                                                              color: '#333' // Color of Y-axis labels
                                                          },
                                                          beginAtZero: true
                                                      }
                                                  }
                                              },
                                            });
                                        });

          <!--Lis charts-->
                                        document.getElementById('generate--chart-lis').addEventListener('click', function(){

                                            const subDepartments = {{ results_lis|map(attribute="sub_department")|list|tojson|safe }};
                                            const blank1 = {{ results_lis|map(attribute="blank1")|list|tojson|safe }};
                                            const blank2 = {{ results_lis|map(attribute="blank2")|list|tojson|safe }};
                                            const opCount = {{ results_lis|map(attribute="op_count")|list|tojson|safe }};
                                            const ipCount = {{ results_lis|map(attribute="ip_count")|list|tojson|safe }};
                                            

                                         // Chart 1: Blank1 vs OP Count
                                         const ctx1 = document.getElementById('chart1').getContext('2d');
                                         new Chart(ctx1, {
                                           type: 'bar',
                                           data: {
                                             labels: subDepartments,
                                             datasets: [
                                               {
                                                 label: 'Services Required from OP',
                                                 data: blank1,
                                                 backgroundColor: 'rgba(54, 162, 235, 0.6)',
                                                 borderColor: 'rgba(54, 162, 235, 1)',
                                                 borderWidth: 1,
                                               },
                                               {
                                                 label: 'OP Count',
                                                 data: opCount,
                                                 backgroundColor: 'rgba(255, 99, 132, 0.6)',
                                                 borderColor: 'rgba(255, 99, 132, 1)',
                                                 borderWidth: 1,
                                               }
                                             ]
                                           },
                                           options: {
                                            plugins: {
                                                legend: {
                                                    labels: {
                                                        font: {
                                                            size: 16, // Font size for legend
                                                            weight: 'bold', // Bold legend text
                                                        },
                                                        color: '#333', // Color of legend text
                                                    }
                                                },
                                                datalabels: {
                                                    color: '#000', // Color of the data labels
                                                    anchor: 'end', // Positioning of the label
                                                    align: 'top', // Alignment of the label
                                                    font: {
                                                        size: 14, // Font size for data labels
                                                        weight: 'bold', // Bold data labels
                                                    },
                                                    formatter: function (value) {
                                                        return value; // Display the value
                                                    }
                                                }
                                            },
                                            scales: {
                                              x: {
                                                  ticks: {
                                                      font: {
                                                          size: 14, // Font size for X-axis labels
                                                          weight: 'bold' // Bold X-axis labels
                                                      },
                                                      color: '#333' // Color of X-axis labels
                                                  }
                                              },
                                              y: {
                                                  ticks: {
                                                      font: {
                                                          size: 14, // Font size for Y-axis labels
                                                          weight: 'bold' // Bold Y-axis labels
                                                      },
                                                      color: '#333' // Color of Y-axis labels
                                                  },
                                                  beginAtZero: true
                                              }
                                          }
                                      },
                                        plugins: [ChartDataLabels] // Register the plugin
                                    });

                                         // Chart 2: Blank2 vs IP Count
                                         const ctx2 = document.getElementById('chart2').getContext('2d');
                                         new Chart(ctx2, {
                                           type: 'bar',
                                           data: {
                                             labels: subDepartments,
                                             datasets: [
                                               {
                                                 label: 'Services Required from IP',
                                                 data: blank2,
                                                 backgroundColor: 'rgba(75, 192, 192, 0.6)',
                                                 borderColor: 'rgba(75, 192, 192, 1)',
                                                 borderWidth: 1,
                                               },
                                               {
                                                 label: 'IP Count',
                                                 data: ipCount,
                                                 backgroundColor: 'rgba(153, 102, 255, 0.6)',
                                                 borderColor: 'rgba(153, 102, 255, 1)',
                                                 borderWidth: 1,
                                               }
                                             ]
                                           },
                                           options: {
                                            plugins: {
                                                legend: {
                                                    labels: {
                                                        font: {
                                                            size: 16, // Font size for legend
                                                            weight: 'bold', // Bold legend text
                                                        },
                                                        color: '#333', // Color of legend text
                                                    }
                                                },
                                                datalabels: {
                                                    color: '#000', // Color of the data labels
                                                    anchor: 'end', // Positioning of the label
                                                    align: 'top', // Alignment of the label
                                                    font: {
                                                        size: 14, // Font size for data labels
                                                        weight: 'bold', // Bold data labels
                                                    },
                                                    formatter: function (value) {
                                                        return value; // Display the value
                                                    }
                                                }
                                            },
                                            scales: {
                                              x: {
                                                  ticks: {
                                                      font: {
                                                          size: 14, // Font size for X-axis labels
                                                          weight: 'bold' // Bold X-axis labels
                                                      },
                                                      color: '#333' // Color of X-axis labels
                                                  }
                                              },
                                              y: {
                                                  ticks: {
                                                      font: {
                                                          size: 14, // Font size for Y-axis labels
                                                          weight: 'bold' // Bold Y-axis labels
                                                      },
                                                      color: '#333' // Color of Y-axis labels
                                                  },
                                                  beginAtZero: true
                                              }
                                          }
                                      },
                                        plugins: [ChartDataLabels] // Register the plugin
                                    });

                                   });
          <!--LIS category charts-->
                                   document.getElementById('generate-category-chart-lis').addEventListener('click', function() {
                                    const labels = {{ lisCategory_json | tojson | safe }};
                                    const opd_data = {{ opd_patient_count_json | tojson | safe }};
                                    const ipd_data = {{ ipd_patient_count_json | tojson | safe }};
                                    

                                       const categoryChart = document.getElementById('lisOpdCategoryChart')
                                       new Chart(categoryChart, {
                                           type: 'pie',
                                           data: {
                                               labels: labels,
                                               datasets: [{
                                                   data: opd_data,
                                                   backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0']
                                               }]
                                           },options: {
                                            responsive: false,
                                            maintainAspectRatio: false,
                                            plugins: {
                                                legend: {
                                                  position: 'right',
                                                  labels: {
                                                    font: {
                                                        size: 14, // Font size for the legend
                                                        weight: 'bold', // Optional: Make the legend text bold
                                                    },
                                                    color: '#000', // Legend text color
                                                }
                                                },datalabels: {
                                                  color: '#000',
                                                  font: {
                                                    size: 14, // Set the font size (in pixels)
                                                    weight: 'bold', // Optional: Make the text bold
                                                },  // Color of the text
                                                  anchor: 'top', // Positioning of the label
                                                  align: 'top', // Alignment of the label
                                                  formatter: function(value) {
                                                      return value; // Display the value
                                                  }
                                              }
                                            }
                                        },plugins: [ChartDataLabels]
                                      });
                                       const categoryChart1 = document.getElementById('lisIpdCategoryChart')
                                       new Chart(categoryChart1, {
                                           type: 'pie',
                                           data: {
                                               labels: labels,
                                               datasets: [{
                                                   data: ipd_data,
                                                   backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0']
                                               }]
                                           },options: {
                                            responsive: false,
                                            maintainAspectRatio: false,
                                            plugins: {
                                                legend: {
                                                  position: 'right',
                                                  labels: {
                                                    font: {
                                                        size: 14, // Font size for the legend
                                                        weight: 'bold', // Optional: Make the legend text bold
                                                    },
                                                    color: '#000', // Legend text color
                                                }
                                                },datalabels: {
                                                  color: '#000',
                                                  font: {
                                                    size: 14, // Set the font size (in pixels)
                                                    weight: 'bold', // Optional: Make the text bold
                                                },  // Color of the text
                                                  anchor: 'top', // Positioning of the label
                                                  align: 'top', // Alignment of the label
                                                  formatter: function(value) {
                                                      return value; // Display the value
                                                  }
                                              }
                                            }
                                        },plugins: [ChartDataLabels]
                                      });
                                   });
          <!--Operation Report-->
                                   document.getElementById('generate-otChart').addEventListener('click', function() {
                                   const minorCtx = document.getElementById('minorOtChart').getContext('2d');
                                   const majorCtx = document.getElementById('majorOtChart').getContext('2d');

                                   // Get dynamic data from the backend (Minor OT)
                                   const minorDepartments = {{ results_ot[1]|map(attribute="department")|list|tojson|safe }};
                                   const minorSurgeriesRequired = {{ results_ot[1]|map(attribute="blank1")|list|tojson|safe }};
                                   const minorPatientGeneral = {{ results_ot[1]|map(attribute="minor_patient_general")|list|tojson|safe }};
                                   const minorGeneral = {{ results_ot[1]|map(attribute="minor_gen")|list|tojson|safe }};
                                   const minorAarogyasri = {{ results_ot[1]|map(attribute="minor_arg")|list|tojson|safe }};
                                   const minorESH = {{ results_ot[1]|map(attribute="minor_esh")|list|tojson|safe }};


                                   // Create Minor OT chart
                                   new Chart(minorCtx, {
                                     type: 'bar',
                                     data: {
                                       labels: minorDepartments,
                                       datasets: [
                                         // Minor Surgeries Required - Standalone
                                         {
                                           label: 'Minor Surgeries Required',
                                           data: minorSurgeriesRequired,
                                           backgroundColor: 'rgba(54, 162, 235, 0.6)',
                                           borderColor: 'rgba(54, 162, 235, 1)',
                                           borderWidth: 1
                                         },
                                         // Stacked Total Count Segregation
                                         {
                                           label: 'Patient General',
                                           data: minorPatientGeneral,
                                           backgroundColor: 'rgba(255, 99, 133, 0.97)',
                                           stack: 'TotalCount'
                                         },
                                         {
                                           label: 'General',
                                           data: minorGeneral,
                                           backgroundColor: 'rgba(255, 206, 86, 0.6)',
                                           stack: 'TotalCount'
                                         },
                                         {
                                           label: 'Aarogyasri',
                                           data: minorAarogyasri,
                                           backgroundColor: 'rgba(153, 102, 255, 0.6)',
                                           stack: 'TotalCount'
                                         },
                                         {
                                           label: 'ESH',
                                           data: minorESH,
                                           backgroundColor: 'rgba(255, 159, 64, 0.6)',
                                           stack: 'TotalCount'
                                         }
                                       ]
                                     },
                                     options: {
                                      plugins: {
                                        legend: {
                                            labels: {
                                                font: {
                                                    size: 16, // Font size for legend
                                                    weight: 'bold', // Bold legend text
                                                },
                                                color: '#333', // Color of legend text
                                            }
                                        },
                                        datalabels: {
                                            color: '#000', // Color of the data labels
                                            anchor: 'end', // Positioning of the label
                                            align: 'top', // Alignment of the label
                                            font: {
                                                size: 14, // Font size for data labels
                                                weight: 'bold', // Bold data labels
                                            },
                                            formatter: function (value) {
                                                return value; // Display the value
                                            }
                                        }
                                    },
                                        scales: {
                                          x: {
                                              ticks: {
                                                  font: {
                                                      size: 14, // Font size for X-axis labels
                                                      weight: 'bold' // Bold X-axis labels
                                                  },
                                                  color: '#333' // Color of X-axis labels
                                              }
                                          },
                                          y: {
                                              ticks: {
                                                  font: {
                                                      size: 14, // Font size for Y-axis labels
                                                      weight: 'bold' // Bold Y-axis labels
                                                  },
                                                  color: '#333' // Color of Y-axis labels
                                              },
                                              beginAtZero: true
                                          }
                                      }
                                  },
                                });
                                   

                                   // Create Major OT chart (unchanged)
                                   const majorDepartments = {{ results_ot[0]|map(attribute="department")|list|tojson|safe }};
                                   const majorSurgeriesRequired = {{ results_ot[0]|map(attribute="blank2")|list|tojson|safe }};
                                   const majorPatientGeneral = {{ results_ot[0]|map(attribute="major_patient_general")|list|tojson|safe }};
                                   const majorGeneral = {{ results_ot[0]|map(attribute="major_gen")|list|tojson|safe }};
                                   const majorAarogyasri = {{ results_ot[0]|map(attribute="major_arg")|list|tojson|safe }};
                                   const majorESH = {{ results_ot[0]|map(attribute="major_esh")|list|tojson|safe }};

                                   new Chart(majorCtx, {
                                     type: 'bar',
                                     data: {
                                       labels: majorDepartments,
                                       datasets: [
                                         {
                                           label: 'Major Surgeries Required',
                                           data: majorSurgeriesRequired,
                                           backgroundColor: 'rgba(54, 162, 235, 0.6)',
                                           borderColor: 'rgba(54, 162, 235, 1)',
                                           borderWidth: 1
                                         },
                                         // Stacked Total Count Segregation
                                         {
                                           label: 'Patient General',
                                           data: majorPatientGeneral,
                                           backgroundColor: 'rgba(255, 99, 133, 0.94)',
                                           stack: 'TotalCount'
                                         },
                                         {
                                           label: 'General',
                                           data: majorGeneral,
                                           backgroundColor: 'rgba(255, 206, 86, 0.6)',
                                           stack: 'TotalCount'
                                         },
                                         {
                                           label: 'Aarogyasri',
                                           data: majorAarogyasri,
                                           backgroundColor: 'rgba(153, 102, 255, 0.6)',
                                           stack: 'TotalCount'
                                         },
                                         {
                                           label: 'ESH',
                                           data: majorESH,
                                           backgroundColor: 'rgba(255, 159, 64, 0.6)',
                                           stack: 'TotalCount'
                                         }
                                       ]
                                     },
                                     options: {
                                      plugins: {
                                        legend: {
                                            labels: {
                                                font: {
                                                    size: 16, // Font size for legend
                                                    weight: 'bold', // Bold legend text
                                                },
                                                color: '#333', // Color of legend text
                                            }
                                        },
                                        datalabels: {
                                            color: '#000', // Color of the data labels
                                            anchor: 'end', // Positioning of the label
                                            align: 'top', // Alignment of the label
                                            font: {
                                                size: 14, // Font size for data labels
                                                weight: 'bold', // Bold data labels
                                            },
                                            formatter: function (value) {
                                                return value; // Display the value
                                            }
                                        }
                                    },
                                        scales: {
                                          x: {
                                              ticks: {
                                                  font: {
                                                      size: 14, // Font size for X-axis labels
                                                      weight: 'bold' // Bold X-axis labels
                                                  },
                                                  color: '#333' // Color of X-axis labels
                                              }
                                          },
                                          y: {
                                              ticks: {
                                                  font: {
                                                      size: 14, // Font size for Y-axis labels
                                                      weight: 'bold' // Bold Y-axis labels
                                                  },
                                                  color: '#333' // Color of Y-axis labels
                                              },
                                              beginAtZero: true
                                          }
                                      }
                                  },
                                });
                                   });
          <!--Biopsy Report-->
                              document.getElementById('generate-chart').addEventListener('click', function () {

                                   const ctx = document.getElementById('biopsyChart').getContext('2d');

                                   // Extracting data for the pie chart
                                   const departments = {{ results_biopsy[:-1]|map(attribute="department")|list|tojson|safe }};
                                   const counts = {{ results_biopsy[:-1]|map(attribute="ip_count")|list|tojson|safe }};

                                   // Creating the pie chart
                                   new Chart(ctx, {
                                       type: 'pie',
                                       data: {
                                           labels: departments,
                                           datasets: [{
                                               label: 'IP Count',
                                               data: counts,
                                               backgroundColor: [
                                                   'rgba(255, 99, 132, 0.2)',
                                                   'rgba(54, 162, 235, 0.2)',
                                                   'rgba(255, 206, 86, 0.2)',
                                                   'rgba(75, 192, 192, 0.2)',
                                                   'rgba(153, 102, 255, 0.2)'
                                               ],
                                               borderColor: [
                                                   'rgba(255, 99, 132, 1)',
                                                   'rgba(54, 162, 235, 1)',
                                                   'rgba(255, 206, 86, 1)',
                                                   'rgba(75, 192, 192, 1)',
                                                   'rgba(153, 102, 255, 1)'
                                               ],
                                               borderWidth: 1
                                           }]
                                       },
                                       options: {
                                        responsive: false,
                                        maintainAspectRatio: false,
                                        plugins: {
                                            legend: {
                                              position: 'right',
                                              labels: {
                                                font: {
                                                    size: 14, // Font size for the legend
                                                    weight: 'bold', // Optional: Make the legend text bold
                                                },
                                                color: '#000', // Legend text color
                                            }
                                            },datalabels: {
                                              color: '#000',
                                              font: {
                                                size: 14, // Set the font size (in pixels)
                                                weight: 'bold', // Optional: Make the text bold
                                            },  // Color of the text
                                              anchor: 'top', // Positioning of the label
                                              align: 'top', // Alignment of the label
                                              formatter: function(value) {
                                                  return value; // Display the value
                                              }
                                          }
                                        }
                                    },plugins: [ChartDataLabels]
                                  });
                                });
 



