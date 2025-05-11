<script>
  import { onMount } from 'svelte';
  import FormularioMovimiento from '$lib/FormularioMovimiento.svelte';
  import ListaMovimientos from '$lib/ListaMovimientos.svelte';
  import Facturacion from '$lib/Facturacion.svelte';
  import DashboardGraficos from '$lib/DashboardGraficos.svelte'

  let tab = "ingresos";
  let movimientos = [];
  let busqueda = "";

  const API = "http://localhost:8001";

  async function cargarMovimientos() {
    const res = await fetch(`${API}/movimientos`);
    movimientos = await res.json();
  }

  async function agregarMovimiento(data) {
    const res = await fetch(`${API}/movimientos`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    if (res.ok) {
      await cargarMovimientos();
    } else {
      console.error("Error al agregar:", res.status, await res.text());
    }
  }

  async function eliminarMovimiento(id) {
    const res = await fetch(`${API}/movimientos/${id}`, {
      method: "DELETE"
    });

    if (res.ok) {
      await cargarMovimientos();
    } else {
      console.error("Error al eliminar:", res.status, await res.text());
    }
  }

  onMount(cargarMovimientos);
</script>

<!-- Fondo general -->
<div class="min-h-screen bg-gradient-to-br from-pink-200 via-fuchsia-100 to-white py-10 px-4">

  <!-- Título -->
  <h1 class="text-4xl sm:text-5xl md:text-6xl font-extrabold text-center mb-10 tracking-wider relative">
    <span class="relative z-10">TITICASH</span>
    <span class="absolute bottom-0 left-1/2 w-1/3 h-1 bg-pink-400 -translate-x-1/2 rounded z-0"></span>
  </h1>

  <!-- Contenedor principal -->
  <div class="w-full max-w-screen-2xl mx-auto px-4 lg:px-8">

    <!-- Tabs -->
    <div class="flex justify-center flex-wrap text-center gap-4 mb-6">

      {#each ["ingresos", "egresos", "movimientos"] as t}
        <button
          class={`px-4 py-2 font-semibold uppercase border-b-2 ${
            tab === t ? "border-black text-black" : "border-transparent text-gray-600"
          }`}
          on:click={() => tab = t}
        >
          {t}
        </button>
      {/each}
    </div>

    <!-- Columnas: contenido + facturación -->
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div class="hidden lg:block">
            <DashboardGraficos movimientos={movimientos} />
        </div>

      <!-- Contenido principal -->
      <div class="lg:col-span-2">
        <div class="w-full bg-white/40 backdrop-blur-sm p-4 sm:p-6 rounded-xl shadow-md">
          <h2 class="text-xl sm:text-2xl font-bold mb-4 text-center">Gestión de {tab}</h2>

          {#if tab === "movimientos"}
            <div class="mb-4">
              <input
                type="text"
                placeholder="Buscar por descripción, categoría o monto"
                bind:value={busqueda}
                class="w-full p-2 border rounded text-sm"
              />
            </div>
            <ListaMovimientos
              tipo="todos"
              movimientos={movimientos}
              filtro={busqueda}
              onEliminar={eliminarMovimiento}
            />
          {:else}
            <FormularioMovimiento tipo={tab} onAgregar={agregarMovimiento} />
            <ListaMovimientos
              tipo={tab}
              movimientos={movimientos}
              onEliminar={eliminarMovimiento}
            />
          {/if}
        </div>
      </div>

      <!-- Facturación -->
      <div>
        <Facturacion movimientos={movimientos} />
      </div>
    </div>
  </div>
</div>
