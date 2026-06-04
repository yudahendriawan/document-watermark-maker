document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const previewWrapper = document.getElementById('preview-wrapper');
    const previewImage = document.getElementById('preview-image');
    const btnChangeImage = document.getElementById('btn-change-image');
    const btnDownload = document.getElementById('btn-download');
    
    // Control Elements
    const watermarkText = document.getElementById('watermark-text');
    const gridMode = document.getElementById('grid-mode');
    const opacitySlider = document.getElementById('opacity');
    const angleSlider = document.getElementById('angle');
    const scaleSlider = document.getElementById('scale');
    const spacingSlider = document.getElementById('spacing');
    const spacingGroup = document.getElementById('spacing-group');
    const colorPicker = document.getElementById('color');
    const colorHex = document.getElementById('color-hex');
    
    // Value Indicators
    const opacityVal = document.getElementById('opacity-val');
    const angleVal = document.getElementById('angle-val');
    const scaleVal = document.getElementById('scale-val');
    const spacingVal = document.getElementById('spacing-val');
    
    const loadingOverlay = document.getElementById('loading-overlay');
    const presetButtons = document.querySelectorAll('.btn-preset');
    
    // Application State
    let currentFile = null;
    let currentBlobUrl = null;
    let debounceTimer = null;
    
    // Format tanggal hari ini
    const today = new Date();
    const dd = String(today.getDate()).padStart(2, '0');
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const yyyy = today.getFullYear();
    const formattedDate = `${dd}-${mm}-${yyyy}`;
    
    // Set default text area value dengan tanggal hari ini
    const defaultText = `KTP UNTUK VERIFIKASI\n[NAMA LAYANAN]\nPADA ${formattedDate}`;
    watermarkText.value = defaultText;
    
    // ----------------------------------------------------
    // Drag & Drop & File Input Handlers
    // ----------------------------------------------------
    
    // Input file sekarang meng-overlay drop zone secara transparan, jadi klik ditangani secara native.
    
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });
    
    // Efek visual dragover
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.add('dragover');
        }, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.remove('dragover');
        }, false);
    });
    
    dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });
    
    btnChangeImage.addEventListener('click', () => {
        // Reset state
        currentFile = null;
        if (currentBlobUrl) {
            URL.revokeObjectURL(currentBlobUrl);
            currentBlobUrl = null;
        }
        fileInput.value = '';
        previewImage.src = '';
        btnDownload.disabled = true;
        
        // Beralih tampilan ke upload zone
        previewWrapper.classList.add('hidden');
        dropZone.classList.remove('hidden');
    });
    
    function handleFileSelect(file) {
        // Validasi tipe file
        if (!file.type.startsWith('image/')) {
            alert('File yang diunggah harus berupa gambar!');
            return;
        }
        
        currentFile = file;
        
        // Beralih tampilan ke preview
        dropZone.classList.add('hidden');
        previewWrapper.classList.remove('hidden');
        btnDownload.disabled = false;
        
        // Panggil render watermark
        triggerUpdate();
    }
    
    // ----------------------------------------------------
    // Event Listeners for Controls
    // ----------------------------------------------------
    
    // Sinkronisasi teks dan auto-update
    watermarkText.addEventListener('input', triggerUpdate);
    
    // Toggle Grid Mode
    gridMode.addEventListener('change', () => {
        if (gridMode.checked) {
            spacingGroup.classList.remove('hidden');
        } else {
            spacingGroup.classList.add('hidden');
        }
        triggerUpdate();
    });
    
    // Slider Handlers
    opacitySlider.addEventListener('input', (e) => {
        opacityVal.textContent = `${e.target.value}%`;
        triggerUpdate();
    });
    
    angleSlider.addEventListener('input', (e) => {
        angleVal.textContent = `${e.target.value}°`;
        triggerUpdate();
    });
    
    scaleSlider.addEventListener('input', (e) => {
        scaleVal.textContent = `${(e.target.value / 10).toFixed(1)}%`;
        triggerUpdate();
    });
    
    spacingSlider.addEventListener('input', (e) => {
        spacingVal.textContent = `${e.target.value}px`;
        triggerUpdate();
    });
    
    // Sinkronisasi Color Picker & Hex Code
    colorPicker.addEventListener('input', (e) => {
        colorHex.value = e.target.value;
        triggerUpdate();
    });
    
    colorHex.addEventListener('input', (e) => {
        let value = e.target.value;
        if (value.startsWith('#') && value.length === 7) {
            colorPicker.value = value;
            triggerUpdate();
        } else if (!value.startsWith('#') && value.length === 6) {
            colorPicker.value = '#' + value;
            colorHex.value = '#' + value;
            triggerUpdate();
        }
    });
    
    // Preset Buttons
    presetButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            let template = btn.getAttribute('data-template');
            // Ganti placeholder tanggal
            template = template.replace('{date}', formattedDate);
            // Ganti karakter '\\n' menjadi newline nyata
            template = template.replace(/\\n/g, '\n');
            
            watermarkText.value = template;
            watermarkText.focus();
            triggerUpdate();
        });
    });
    
    // Download Action
    btnDownload.addEventListener('click', () => {
        if (!currentBlobUrl) return;
        
        const originalName = currentFile.name;
        const ext = originalName.substring(originalName.lastIndexOf('.'));
        const baseName = originalName.substring(0, originalName.lastIndexOf('.'));
        
        const downloadLink = document.createElement('a');
        downloadLink.href = currentBlobUrl;
        downloadLink.download = `${baseName}_watermarked${ext}`;
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
    });
    
    // ----------------------------------------------------
    // Watermarking Logic & API Call (Debounced)
    // ----------------------------------------------------
    
    function triggerUpdate() {
        if (!currentFile) return;
        
        // Batalkan timer debounce yang sedang berjalan
        if (debounceTimer) {
            clearTimeout(debounceTimer);
        }
        
        // Beri jeda 250ms agar server tidak terlalu sering dipanggil saat slider digeser cepat
        debounceTimer = setTimeout(sendWatermarkRequest, 250);
    }
    
    async function sendWatermarkRequest() {
        if (!currentFile) return;
        
        loadingOverlay.classList.remove('hidden');
        
        const formData = new FormData();
        formData.append('file', currentFile);
        formData.append('text', watermarkText.value);
        formData.append('opacity', opacitySlider.value);
        formData.append('angle', angleSlider.value);
        // Konversi skala persen (10-100) menjadi desimal (0.01 - 0.1) untuk API
        formData.append('scale', (scaleSlider.value / 1000).toFixed(4));
        formData.append('grid', gridMode.checked);
        formData.append('spacing', spacingSlider.value);
        formData.append('color', colorHex.value);
        
        try {
            const response = await fetch('/api/watermark', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || 'Terjadi kesalahan sistem');
            }
            
            // Baca response sebagai blob gambar
            const blob = await response.blob();
            
            // Hapus object URL lama agar tidak boros memori browser
            if (currentBlobUrl) {
                URL.revokeObjectURL(currentBlobUrl);
            }
            
            // Buat object URL baru untuk preview
            currentBlobUrl = URL.createObjectURL(blob);
            previewImage.src = currentBlobUrl;
            
        } catch (error) {
            console.error('Error watermarking image:', error);
            alert(`Gagal memberi watermark: ${error.message}`);
        } finally {
            loadingOverlay.classList.add('hidden');
        }
    }
});
