<script>
  import Chart from 'chart.js/auto';
  export let movimientos = [];

  let pieChart;
  let barChart;
  let pieCanvas;
  let barCanvas;

  // Destruir anteriores
  function limpiarCharts() {
    pieChart?.destroy();
    barChart?.destroy();
  }

  // Reaccionar cuando hay movimientos
  $: if (movimientos.length) {
    limpiarCharts();

    // PIE CHART
    const ingresos = movimientos.filter(m => m.tipo === "Ingreso").length;
    const egresos = movimientos.filter(m => m.tipo === "Egreso").length;

    pieChart = new Chart(pieCanvas, {
      type: 'pie',
      data: {
        labels: ['Ingresos', 'Egresos'],
        datasets: [{
          data: [ingresos, egresos],
          backgroundColor: ['#10b981', '#ef4444']
        }]
      },
      options: {
        plugins: { legend: { position: 'bottom' } }
      }
    });

    // BAR CHART
    const ingresosMensuales = movimientos
      .filter(m => m.tipo === "Ingreso")
      .reduce((acc, m) => {
        const fecha = new Date(m.fecha);
        const key = fecha.toLocaleString('default', { month: 'short' }) + ' ' + fecha.getFullYear();
        acc[key] = (acc[key] || 0) + m.monto;
        return acc;
      }, {});

    const etiquetas = Object.keys(ingresosMensuales).slice(-6);
    const montos = etiquetas.map(e => ingresosMensuales[e]);

    barChart = new Chart(barCanvas, {
      type: 'bar',
      data: {
        labels: etiquetas,
        datasets: [{
          label: 'Ingresos por mes',
          data: montos,
          backgroundColor: '#10b981'
        }]
      },
      options: {
        scales: {
          y: { beginAtZero: true }
        },
        plugins: { legend: { display: false } }
      }
    });
  }
</script>

<div class="bg-white/30 backdrop-blur-lg rounded-xl p-4 shadow-xl text-sm space-y-6">
  <h3 class="text-lg font-bold text-center text-gray-800">Visualizaciones</h3>

  {#if movimientos.length === 0}
    <p class="text-center text-gray-500 py-8">No hay datos para graficar.</p>
  {:else}
    <div>
      <h4 class="font-semibold text-center mb-2 text-gray-700">Distribución</h4>
      <canvas bind:this={pieCanvas}></canvas>
    </div>

    <div>
      <h4 class="font-semibold text-center mb-2 text-gray-700">Ingresos mensuales</h4>
      <canvas bind:this={barCanvas}></canvas>
    </div>
  {/if}
</div>
