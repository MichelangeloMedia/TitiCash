<script>
  export let tipo;
  export let onAgregar;

let nuevo;

$: nuevo = {
  tipo: tipo === "ingresos" ? "Ingreso" : "Egreso",
  monto: null,
  descripcion: "",
  metodo: "Efectivo",
  categoria: "General",
  fecha: new Date().toISOString().slice(0, 10)
};

  const categoriasIngresos =["Locales", "RTV", "C4", "Familia", "➕ Añadir nueva categoría"].sort();

  const categoriasEgresos = [
    "Alquiler", "Servicios", "Club", "Colegio", "Actividades Juana",
    "Salidas", "Supermercado", "Apps", "Tarjeta", "Prestamos", "AFIP",
    "Pelotitideces", "Personal", "➕ Añadir nueva categoría"
  ].sort();

  $: categorias = tipo === "ingresos" ? categoriasIngresos : categoriasEgresos;

  let mostrandoCampoCategoria = false;
  let nuevaCategoria = "";

  function agregarCategoriaPersonalizada(nombre) {
    if (tipo === "ingresos") {
      categoriasIngresos.splice(-1, 0, nombre);
    } else {
      categoriasEgresos.splice(-1, 0, nombre);
    }
  }

  function submitForm() {
    if (mostrandoCampoCategoria && nuevaCategoria.trim()) {
      agregarCategoriaPersonalizada(nuevaCategoria.trim());
      nuevo.categoria = nuevaCategoria.trim();
      mostrandoCampoCategoria = false;
      nuevaCategoria = "";
    }

    const data = {
      ...nuevo,
      fecha: new Date(nuevo.fecha).toISOString()
    };
    onAgregar(data);

    nuevo = {
      tipo: tipo === "ingresos" ? "Ingreso" : "Egreso",
      monto: null,
      descripcion: "",
      metodo: "Efectivo",
      categoria: "General",
      fecha: new Date().toISOString().slice(0, 10)
    };
  }
</script>

<div class="space-y-4 mb-6 text-sm">
  <input type="number" placeholder="Monto en pesos" bind:value={nuevo.monto} class="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-pink-400" />
  <input type="text" placeholder="Descripción" bind:value={nuevo.descripcion} class="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-pink-400" />

  <select bind:value={nuevo.metodo} class="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-pink-400">
    <option value="Efectivo">Efectivo</option>
    <option value="Transferencia">Transferencia</option>
    <option value="Crédito">Crédito</option>
  </select>

  <select bind:value={nuevo.categoria} class="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-pink-400" on:change={(e) => {
    mostrandoCampoCategoria = e.target.value === "➕ Añadir nueva categoría";
  }}>
    {#each categorias as c}
      <option value={c}>{c}</option>
    {/each}
  </select>

  {#if mostrandoCampoCategoria}
    <input type="text" placeholder="Nueva categoría" bind:value={nuevaCategoria} class="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-pink-400" />
  {/if}

  <input type="date" bind:value={nuevo.fecha} class="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-pink-400" />

  <button type="button" class="bg-black text-white px-4 py-2 rounded hover:bg-gray-800 transition" on:click={submitForm}>Agregar {tipo}</button>
</div>
