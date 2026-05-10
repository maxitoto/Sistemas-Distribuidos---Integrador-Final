async function test(method, path, body = null) {
    const consoleBox = document.getElementById('response-console');
    consoleBox.innerHTML = "Enviando petición a " + path + "...";

    const options = {
        method: method,
        headers: { 'Content-Type': 'application/json' }
    };
    if (body) options.body = JSON.stringify(body);

    try {

        const response = await fetch(path, options);
        const data = await response.json();
        
        consoleBox.innerHTML = `// Status: ${response.status} ${response.statusText}\n` + 
                                JSON.stringify(data, null, 4);
    } catch (error) {
        consoleBox.innerHTML = "// ERROR DE CONEXIÓN\n" + error;
    }
}