<script>
  import jsPDF from 'jspdf';
  import autoTable from 'jspdf-autotable';

  export let movimientos = [];
  export let desde = "";
  export let hasta = "";

  let pagina = 1;
  const porPagina = 10;

  // Filtrar ingresos por criterios
  $: filtrados = movimientos.filter(m =>
    m.tipo === "Ingreso" &&
    m.metodo === "Transferencia" &&
    m.monto > 10000 &&
    (!desde || new Date(m.fecha) >= new Date(desde)) &&
    (!hasta || new Date(m.fecha) <= new Date(hasta))
  );

  $: totalPaginas = Math.ceil(filtrados.length / porPagina);
  $: paginados = filtrados.slice((pagina - 1) * porPagina, pagina * porPagina);
  $: totalFacturar = filtrados.reduce((sum, m) => sum + m.monto, 0);

  function formatearFecha(iso) {
    const f = new Date(iso);
    return `${f.getDate().toString().padStart(2, "0")}-${(f.getMonth() + 1).toString().padStart(2, "0")}-${f.getFullYear()}`;
  }

  $: if (pagina > totalPaginas) pagina = 1;

  function exportarPDF() {
    const doc = new jsPDF();
    doc.setFontSize(16);
    doc.text("Facturación", 14, 20);

    autoTable(doc, {
      head: [["Fecha", "Descripción", "Categoría", "Monto"]],
      body: filtrados.map(m => [
        new Date(m.fecha).toLocaleDateString("es-AR"),
        m.descripcion,
        m.categoria,
        `$${m.monto.toLocaleString("es-AR")}`
      ]),
      startY: 30
    });

    doc.setFontSize(14);
    doc.text(`TOTAL A FACTURAR: $${totalFacturar.toLocaleString("es-AR")}`, 14, doc.lastAutoTable.finalY + 10);
    doc.save("facturacion.pdf");
  }
</script>

<div class="bg-white/40 backdrop-blur-sm rounded-xl p-4 shadow-md">
  <h3 class="text-lg font-bold mb-4 text-center">Facturación</h3>

  <!-- Rango de fechas -->
  <div class="flex flex-col gap-2 mb-4 text-sm">
    <label>
      Desde:
      <input type="date" bind:value={desde} class="w-full p-2 border rounded mt-1" />
    </label>
    <label>
      Hasta:
      <input type="date" bind:value={hasta} class="w-full p-2 border rounded mt-1" />
    </label>
  </div>

  <!-- Lista de movimientos -->
  <ul class="divide-y text-sm sm:text-base mb-4">
    {#each paginados as m}
      <li class="py-2 flex justify-between items-center">
        <span class="text-gray-800">{m.descripcion} – ${m.monto.toLocaleString("es-AR")}</span>
        <span class="text-gray-500">{formatearFecha(m.fecha)}</span>
      </li>
    {:else}
      <li class="py-2 text-gray-500 text-center">No hay ingresos en ese rango.</li>
    {/each}
  </ul>

  <!-- Navegación -->
  {#if totalPaginas > 1}
    <div class="flex justify-center gap-4 mb-4">
      <button on:click={() => pagina--} disabled={pagina === 1} class="text-blue-700 text-sm disabled:text-gray-400">←</button>
      <span class="text-sm">Página {pagina} de {totalPaginas}</span>
      <button on:click={() => pagina++} disabled={pagina === totalPaginas} class="text-blue-700 text-sm disabled:text-gray-400">→</button>
    </div>
  {/if}

  <!-- Total a facturar -->
  <div class={`text-xl sm:text-2xl font-bold text-center mt-4 ${
    totalFacturar >= 880000 ? "text-red-700"
    : totalFacturar >= 780000 ? "text-orange-500"
    : "text-fuchsia-700"
  }`}>
    TOTAL A FACTURAR: $ {totalFacturar.toLocaleString("es-AR")}
  </div>

  <!-- Mensaje condicional -->
  {#if totalFacturar >= 880000}
    <p class="text-center mt-2 text-sm text-red-600 font-semibold">
      Superaste tu total permitido
    </p>
  {:else if totalFacturar >= 780000}
    <p class="text-center mt-2 text-sm text-orange-500 font-semibold">
      Estás a $ {(880000 - totalFacturar).toLocaleString("es-AR")} de alcanzar tu total permitido
    </p>
  {/if}

  <!-- Botón de exportar -->
  <button
    type="button"
    on:click={exportarPDF}
    class="mt-4 bg-black text-white px-4 py-2 rounded hover:bg-gray-800 w-full"
  >
    Exportar PDF
  </button>
</div>
