<script>
  import Chart from 'chart.js/auto';
  import { onMount, tick } from 'svelte';
  export let movimientos = [];

  let pieChart, barChart, balanceChart, egresosCatChart, metodoChart;
  let pieCanvas, barCanvas, balanceCanvas, egresosCatCanvas, metodoCanvas;
  let activeTab = 'distribucion';
  let loadingChart = false;

  function limpiarCharts() {
    pieChart?.destroy();
    barChart?.destroy();
    balanceChart?.destroy();
  }

  function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  $: if (movimientos.length) {
    limpiarCharts();

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
  }

  async function renderEgresosPorCategoria() {
    loadingChart = true;
    egresosCatChart?.destroy();
    await tick();

    setTimeout(() => {
      const egresosPorCategoria = movimientos
        .filter(m => m.tipo === "Egreso")
        .reduce((acc, m) => {
          acc[m.categoria] = (acc[m.categoria] || 0) + m.monto;
          return acc;
        }, {});

      const topCategorias = Object.entries(egresosPorCategoria)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5);

      const etiquetasCat = topCategorias.map(([c]) => c);
      const valoresCat = topCategorias.map(([, v]) => v);

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
      loadingChart = false;
    }, 100);
  }

    async function renderIngresosPorCategoria() {
    loadingChart = true;
    ingresosCatChart?.destroy();
    await tick();

    setTimeout(() => {
      const ingresosPorCategoria = movimientos
        .filter(m => m.tipo === "Ingreso")
        .reduce((acc, m) => {
          acc[m.categoria] = (acc[m.categoria] || 0) + m.monto;
          return acc;
        }, {});

      const topCategorias = Object.entries(ingresosPorCategoria)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5);

      const etiquetasCat = topCategorias.map(([c]) => c);
      const valoresCat = topCategorias.map(([, v]) => v);

      ingresosCatChart = new Chart(ingresosCatCanvas, {
        type: 'bar',
        data: {
          labels: etiquetasCat,
          datasets: [{
            label: 'Ingresos por categoría',
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
      loadingChart = false;
    }, 100);
  }

  

  $: if (activeTab === 'egresosCat' && movimientos.length) {
    renderEgresosPorCategoria();
  }

  $: if (activeTab === 'ingresosCat' && movimientos.length) {
    renderIngresosPorMetodo();
  }
</script>

<div class="bg-white/30 backdrop-blur-lg rounded-xl p-4 shadow-xl text-sm space-y-4 w-full">
  <h3 class="text-lg font-bold text-center text-gray-800">Visualizaciones</h3>
  {#if movimientos.length === 0}
    <p class="text-center text-gray-500 py-8">No hay datos para graficar.</p>
  {:else}
    <div class="flex flex-wrap justify-center gap-2 text-xs sm:text-sm">
      <button on:click={() => activeTab = 'distribucion'} class:font-bold={activeTab === 'distribucion'}>Distribución</button>
      <button on:click={() => activeTab = 'ingresos'} class:font-bold={activeTab === 'ingresos'}>Ingresos por mes</button>
      <button on:click={() => activeTab = 'balance'} class:font-bold={activeTab === 'balance'}>Balance mensual</button>
      <button on:click={() => activeTab = 'egresosCat'} class:font-bold={activeTab === 'egresosCat'}>Egresos por categoría</button>
      <button on:click={() => activeTab = 'ingresosCat'} class:font-bold={activeTab === 'ingresosCat'}>Ingresos por categoría</button>
    </div>

    {#if activeTab === 'distribucion'}
      <div>
        <h4 class="font-semibold text-center mb-2 text-gray-700">Distribución Ingresos / Egresos</h4>
        <canvas bind:this={pieCanvas} class="w-full max-w-full"></canvas>
      </div>
    {/if}

    {#if activeTab === 'ingresos'}
      <div>
        <h4 class="font-semibold text-center mb-2 text-gray-700">Ingresos mensuales</h4>
        <canvas bind:this={barCanvas} class="w-full max-w-full"></canvas>
      </div>
    {/if}

    {#if activeTab === 'balance'}
      <div>
        <h4 class="font-semibold text-center mb-2 text-gray-700">Balance mensual</h4>
        <canvas bind:this={balanceCanvas} class="w-full max-w-full"></canvas>
      </div>
    {/if}

    {#if activeTab === 'egresosCat'}
      {#if loadingChart}
        <p class="text-center text-sm text-gray-500">Cargando gráfico...</p>
      {/if}
      <div>
        <h4 class="font-semibold text-center mb-2 text-gray-700">Egresos por categoría</h4>
        <canvas bind:this={egresosCatCanvas} class="w-full max-w-full"></canvas>
      </div>
    {/if}

    {#if activeTab === 'metodo'}
      {#if loadingChart}
        <p class="text-center text-sm text-gray-500">Cargando gráfico...</p>
      {/if}
      <div>
        <h4 class="font-semibold text-center mb-2 text-gray-700">Ingresos por categoría</h4>
        <canvas bind:this={ingresosCatCanvas} class="w-full max-w-full"></canvas>
      </div>
    {/if}

    <div class="flex justify-center mt-6">
      <button on:click={scrollToTop} class="text-sm text-blue-600 underline hover:text-blue-800">
        ⬆ Volver arriba
      </button>
    </div>
  {/if}
</div>