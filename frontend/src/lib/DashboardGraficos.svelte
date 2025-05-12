<script>
  import Chart from 'chart.js/auto';
  export let movimientos = [];

  let pieChart, barChart, balanceChart, egresosCatChart, metodoChart;
  let pieCanvas, barCanvas, balanceCanvas, egresosCatCanvas, metodoCanvas;

  function limpiarCharts() {
    pieChart?.destroy();
    barChart?.destroy();
    balanceChart?.destroy();
    egresosCatChart?.destroy();
    metodoChart?.destroy();
  }

  $: if (movimientos.length) {
    limpiarCharts();

    // PIE CHART: Distribución total ingresos vs egresos
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

    // BARRAS: Ingresos por mes
    const ingresosMensuales = movimientos
      .filter(m => m.tipo === "Ingreso")
      .reduce((acc, m) => {
        const fecha = new Date(m.fecha);
        const key = fecha.toLocaleString('default', { month: 'short' }) + ' ' + fecha.getFullYear();
        acc[key] = (acc[key] || 0) + m.monto;
        return acc;
      }, {});

    const etiquetasMeses = Object.keys(ingresosMensuales).slice(-6);
    const montosMeses = etiquetasMeses.map(e => ingresosMensuales[e]);

    barChart = new Chart(barCanvas, {
      type: 'bar',
      data: {
        labels: etiquetasMeses,
        datasets: [{
          label: 'Ingresos por mes',
          data: montosMeses,
          backgroundColor: '#10b981'
        }]
      },
      options: {
        scales: { y: { beginAtZero: true } },
        plugins: { legend: { display: false } }
      }
    });

    // BALANCE por mes (ingresos - egresos)
    const balanceMensual = {};
    movimientos.forEach(m => {
      const fecha = new Date(m.fecha);
      const mes = fecha.toLocaleString('default', { month: 'short' }) + ' ' + fecha.getFullYear();
      balanceMensual[mes] = balanceMensual[mes] || 0;
      balanceMensual[mes] += m.tipo === "Ingreso" ? m.monto : -m.monto;
    });
    const etiquetasBalance = Object.keys(balanceMensual).slice(-6);
    const valoresBalance = etiquetasBalance.map(e => balanceMensual[e]);

    balanceChart = new Chart(balanceCanvas, {
      type: 'bar',
      data: {
        labels: etiquetasBalance,
        datasets: [{
          label: 'Balance mensual',
          data: valoresBalance,
          backgroundColor: valoresBalance.map(v => v >= 0 ? '#10b981' : '#ef4444')
        }]
      },
      options: {
        scales: { y: { beginAtZero: true } },
        plugins: { legend: { display: false } }
      }
    });

    // EGRESOS por categoría
    const egresosPorCategoria = movimientos
      .filter(m => m.tipo === "Egreso")
      .reduce((acc, m) => {
        acc[m.categoria] = (acc[m.categoria] || 0) + m.monto;
        return acc;
      }, {});

    const etiquetasCat = Object.keys(egresosPorCategoria);
    const valoresCat = etiquetasCat.map(c => egresosPorCategoria[c]);

    egresosCatChart = new Chart(egresosCatCanvas, {
      type: 'bar',
      data: {
        labels: etiquetasCat,
        datasets: [{
          label: 'Egresos por categoría',
          data: valoresCat,
          backgroundColor: '#ef4444'
        }]
      },
      options: {
        indexAxis: 'y',
        scales: { x: { beginAtZero: true } },
        plugins: { legend: { display: false } }
      }
    });

    // METODOS de ingreso
    const ingresosPorMetodo = movimientos
      .filter(m => m.tipo === "Ingreso")
      .reduce((acc, m) => {
        acc[m.metodo] = (acc[m.metodo] || 0) + m.monto;
        return acc;
      }, {});

    const etiquetasMetodo = Object.keys(ingresosPorMetodo);
    const valoresMetodo = etiquetasMetodo.map(m => ingresosPorMetodo[m]);

    metodoChart = new Chart(metodoCanvas, {
      type: 'doughnut',
      data: {
        labels: etiquetasMetodo,
        datasets: [{
          data: valoresMetodo,
          backgroundColor: ['#10b981', '#3b82f6', '#f59e0b']
        }]
      },
      options: {
        plugins: { legend: { position: 'bottom' } }
      }
    });
  }
</script>

<div class="bg-white/30 backdrop-blur-lg rounded-xl p-4 shadow-xl text-sm space-y-6">
  <h3 class="text-lg font-bold text-center text-gray-800">Visualizaciones</h3>

  {#if movimientos.length === 0}
    <p class="text-center text-gray-500 py-8">No hay datos para graficar.</p>
  {:else}
    <div class="space-y-6">
      <div>
        <h4 class="font-semibold text-center mb-2 text-gray-700">Distribución Ingresos / Egresos</h4>
        <canvas bind:this={pieCanvas} class="w-full max-w-full"></canvas>
      </div>

      <div>
        <h4 class="font-semibold text-center mb-2 text-gray-700">Ingresos mensuales</h4>
        <canvas bind:this={barCanvas} class="w-full max-w-full"></canvas>
      </div>

      <div>
        <h4 class="font-semibold text-center mb-2 text-gray-700">Balance mensual</h4>
        <canvas bind:this={balanceCanvas} class="w-full max-w-full"></canvas>
      </div>

      <div>
        <h4 class="font-semibold text-center mb-2 text-gray-700">Egresos por categoría</h4>
        <canvas bind:this={egresosCatCanvas} class="w-full max-w-full"></canvas>
      </div>

      <div>
        <h4 class="font-semibold text-center mb-2 text-gray-700">Ingresos por método</h4>
        <canvas bind:this={metodoCanvas} class="w-full max-w-full"></canvas>
      </div>
    </div>
  {/if}
</div>