<script>
  export let tipo;
  export let movimientos = [];
  export let filtro = "";
  export let onEliminar;

  let pagina = 1;
  const porPagina = tipo === "todos" ? 15 : 5;

  let mostrarConfirmacion = false;
  let idAEliminar = null;

  function formatearFecha(iso) {
    const f = new Date(iso);
    return `${f.getDate().toString().padStart(2, "0")}-${(f.getMonth() + 1).toString().padStart(2, "0")}-${f.getFullYear()}`;
  }

  function pedirConfirmacion(id) {
    idAEliminar = id;
    mostrarConfirmacion = true;
  }

  function confirmarEliminacion() {
    if (idAEliminar) {
      onEliminar(idAEliminar);
    }
    cerrarModal();
  }

  function cerrarModal() {
    mostrarConfirmacion = false;
    idAEliminar = null;
  }

  $: filtrados = tipo === "todos"
    ? movimientos.filter(m =>
        m.descripcion?.toLowerCase().includes(filtro.toLowerCase()) ||
        m.categoria?.toLowerCase().includes(filtro.toLowerCase()) ||
        String(m.monto).includes(filtro)
      )
    : movimientos.filter(m => {
        const tipoDb = m.tipo?.toLowerCase();
        return tipo === "ingresos" ? tipoDb === "ingreso" : tipoDb === "egreso";
      });

  $: ordenados = [...filtrados].sort((a, b) => new Date(b.fecha) - new Date(a.fecha));
  $: totalPaginas = Math.ceil(ordenados.length / porPagina);
  $: paginados = ordenados.slice((pagina - 1) * porPagina, pagina * porPagina);
  $: if (pagina > totalPaginas) pagina = 1;
</script>

<ul class="divide-y mt-4 text-sm sm:text-base">
  {#each paginados as m (m._id || m.id)}
    <li class="py-2 flex flex-col sm:flex-row sm:justify-between sm:items-center gap-2 border-b">
      <span>
        <span class={`font-semibold ${m.tipo === 'Ingreso' ? 'text-green-600' : 'text-red-600'}`}>
          {m.tipo === "Ingreso" ? "+ " : "- "}
          ${m.monto.toLocaleString("es-AR")}
          {m.metodo === "Efectivo" ? " 💸" : ""}
          {m.metodo === "Transferencia" ? " 💳" : ""}
          {m.metodo === "Transferencia" && m.tipo === "Ingreso" && m.monto >= 10000 ? " 🧾" : ""}
        </span>
        – {m.descripcion} ({m.categoria})
      </span>
      <div class="flex items-center gap-2 justify-between sm:justify-end">
        <span class="text-gray-500">{formatearFecha(m.fecha)}</span>
        <button
          on:click={() => pedirConfirmacion(m._id || m.id)}
          class="text-red-500 hover:text-red-700 text-sm"
          title="Eliminar"
        >
          🗑️
        </button>
      </div>
    </li>
  {:else}
    <li class="py-2 text-gray-500">No hay resultados para esta categoría.</li>
  {/each}
</ul>

{#if totalPaginas > 1}
  <div class="flex justify-center mt-4 gap-4">
    <button on:click={() => pagina--} disabled={pagina === 1} class="text-sm text-blue-700 disabled:text-gray-400">
      ← Anterior
    </button>
    <span class="text-sm">Página {pagina} de {totalPaginas}</span>
    <button on:click={() => pagina++} disabled={pagina === totalPaginas} class="text-sm text-blue-700 disabled:text-gray-400">
      Siguiente →
    </button>
  </div>
{/if}

{#if mostrarConfirmacion}
  <div class="fixed inset-0 backdrop-blur-sm bg-white/10 flex items-center justify-center z-50 p-4">
    <div class="bg-white rounded-lg shadow p-6 w-full max-w-sm text-center space-y-4">
      <h3 class="text-lg font-semibold">¿Eliminar movimiento?</h3>
      <p class="text-sm text-gray-600">Esta acción no se puede deshacer.</p>
      <div class="flex flex-col sm:flex-row justify-center gap-3">
        <button
          on:click={confirmarEliminacion}
          class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
        >
          Eliminar
        </button>
        <button
          on:click={cerrarModal}
          class="bg-gray-300 text-gray-800 px-4 py-2 rounded hover:bg-gray-400"
        >
          Cancelar
        </button>
      </div>
    </div>
  </div>
{/if}
