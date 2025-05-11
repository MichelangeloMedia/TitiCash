<script>
  export let tipo;
  export let onAgregar;

  let nuevo = {
    tipo: tipo === "ingresos" ? "Ingreso" : "Egreso",
    monto: null,
    descripcion: "",
    metodo: "Efectivo",
    categoria: "General",
    fecha: new Date().toISOString().slice(0, 10)
  };

  let categorias = ["General", "Comida", "Servicios", "Transporte", "➕ Añadir nueva categoría"];
  let mostrandoCampoCategoria = false;
  let nuevaCategoria = "";

  function submitForm() {
    if (mostrandoCampoCategoria && nuevaCategoria.trim()) {
      categorias = [...categorias.slice(0, -1), nuevaCategoria.trim(), "➕ Añadir nueva categoría"];
      nuevo.categoria = nuevaCategoria.trim();
      mostrandoCampoCategoria = false;
      nuevaCategoria = "";
    }

    const data = {
      ...nuevo,
      fecha: new Date(nuevo.fecha).toISOString()
    };
    onAgregar(data);

    // Resetear
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

<div class="space-y-4 mb-6">
  <input type="number" placeholder="Monto en pesos" bind:value={nuevo.monto} class="w-full p-2 border rounded" />
  <input type="text" placeholder="Descripción" bind:value={nuevo.descripcion} class="w-full p-2 border rounded" />

  <select bind:value={nuevo.metodo} class="w-full p-2 border rounded">
    <option value="Efectivo">Efectivo</option>
    <option value="Transferencia">Transferencia</option>
    <option value="Débito">Débito</option>
    <option value="Crédito">Crédito</option>
  </select>

  <select bind:value={nuevo.categoria} class="w-full p-2 border rounded" on:change={(e) => {
    if (e.target.value === "➕ Añadir nueva categoría") {
      mostrandoCampoCategoria = true;
    } else {
      mostrandoCampoCategoria = false;
    }
  }}>
    {#each categorias as c}
      <option value={c}>{c}</option>
    {/each}
  </select>

  {#if mostrandoCampoCategoria}
    <input type="text" placeholder="Nueva categoría" bind:value={nuevaCategoria} class="w-full p-2 border rounded" />
  {/if}

  <input type="date" bind:value={nuevo.fecha} class="w-full p-2 border rounded" />

  <button class="bg-black text-white px-4 py-2 rounded" on:click={submitForm}>Agregar {tipo}</button>
</div>
