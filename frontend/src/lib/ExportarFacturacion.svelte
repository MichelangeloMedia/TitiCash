<script>
  let jsPDF;
  export let movimientos = [];

  let desde = "";
  let hasta = "";

  $: filtrados = movimientos.filter(m =>
    m.tipo === "Ingreso" &&
    m.metodo === "Transferencia" &&
    m.monto >= 10000 &&
    (!desde || new Date(m.fecha) >= new Date(desde)) &&
    (!hasta || new Date(m.fecha) <= new Date(hasta))
  );

  $: totalFacturar = filtrados.reduce((acc, m) => acc + m.monto, 0);

  async function exportarPDF() {
    if (!jsPDF) {
      const module = await import('jspdf');
      jsPDF = module.default || module;
    }

    const doc = new jsPDF();
    doc.setFontSize(16);
    doc.text("Facturación", 14, 20);

    doc.autoTable({
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

<div class="space-y-4 text-sm">
  <div class="flex flex-col sm:flex-row gap-4 items-start sm:items-center">
    <label class="flex flex-col">
      Desde:
      <input type="date" bind:value={desde} class="p-2 border border-gray-300 rounded" />
    </label>
    <label class="flex flex-col">
      Hasta:
      <input type="date" bind:value={hasta} class="p-2 border border-gray-300 rounded" />
    </label>
    <button type="button" on:click={exportarPDF} class="bg-black text-white px-4 py-2 rounded hover:bg-gray-800 transition">Exportar PDF</button>
  </div>
</div>
