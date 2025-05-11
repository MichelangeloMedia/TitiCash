<script>
  let jsPDF;
  let autoTable;
  export let movimientos = [];

  let desde = "";
  let hasta = "";

  $: filtrados = movimientos.filter(m => {
    const fecha = new Date(m.fecha);
    const desdeOk = !desde || fecha >= new Date(desde);
    const hastaOk = !hasta || fecha <= new Date(hasta);
    return desdeOk && hastaOk;
  });

async function exportarPDF() {
  if (!jsPDF) {
    const jsPDFModule = await import('jspdf');
    jsPDF = jsPDFModule.default || jsPDFModule;
  }

  if (!autoTable) {
    const autoTableModule = await import('jspdf-autotable');
    autoTable = autoTableModule.default || autoTableModule;
  }

  const doc = new jsPDF();
  doc.setFontSize(16);
  doc.text("Movimientos", 14, 20);

  autoTable(doc, {
  head: [["Fecha", "Tipo", "Descripción", "Categoría", "Monto", "Método"]],
  body: filtrados.map(m => [
    new Date(m.fecha).toLocaleDateString("es-AR"),
    m.tipo,
    m.descripcion,
    m.categoria,
    `$${m.monto.toLocaleString("es-AR")}`,
    m.metodo
  ]),
  startY: 30
});

  doc.save("movimientos.pdf");
}
</script>

<div class="space-y-4 mb-6 text-sm">
  <div class="flex flex-col sm:flex-row gap-4 items-start sm:items-center">
    <label class="flex flex-col">
      Desde:
      <input type="date" bind:value={desde} class="p-2 border border-gray-300 rounded" />
    </label>
    <label class="flex flex-col">
      Hasta:
      <input type="date" bind:value={hasta} class="p-2 border border-gray-300 rounded" />
    </label>
    <button type="button" on:click={exportarPDF} class="bg-black text-white px-4 py-2 rounded hover:bg-gray-800 transition">
      Exportar PDF
    </button>
  </div>
</div>
