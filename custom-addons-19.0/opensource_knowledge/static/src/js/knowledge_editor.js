/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onWillStart, onMounted } from "@odoo/owl";

export class KnowledgeEditor extends Component {
    static template = "opensource_knowledge.KnowledgeEditor";
    
    setup() {
        onWillStart(this.onWillStart);
        onMounted(this.onMounted);
    }
    
    async onWillStart() {
        // Initialize editor configuration
        this.editorConfig = {
            toolbar: [
                ['style', ['style']],
                ['font', ['bold', 'italic', 'underline', 'clear']],
                ['fontname', ['fontname']],
                ['color', ['color']],
                ['para', ['ul', 'ol', 'paragraph']],
                ['table', ['table']],
                ['insert', ['link', 'picture', 'video']],
                ['view', ['fullscreen', 'codeview', 'help']]
            ],
            height: 400,
            minHeight: 200,
            placeholder: 'Start writing your knowledge article...',
            callbacks: {
                onChange: this.onContentChange.bind(this),
                onImageUpload: this.onImageUpload.bind(this)
            }
        };
    }
    
    onMounted() {
        // Initialize the editor
        this.initializeEditor();
    }
    
    initializeEditor() {
        const editorElement = this.el.querySelector('.knowledge-editor');
        if (editorElement) {
            // Initialize HTML editor (using web_editor if available)
            this.editor = editorElement;
            this.setupToolbar();
        }
    }
    
    setupToolbar() {
        // Add custom toolbar items
        const toolbar = this.el.querySelector('.knowledge-toolbar');
        if (toolbar) {
            this.addTemplateButton(toolbar);
            this.addLinkButton(toolbar);
            this.addImageButton(toolbar);
            this.addTableButton(toolbar);
        }
    }
    
    addTemplateButton(toolbar) {
        const button = document.createElement('button');
        button.className = 'btn btn-sm btn-secondary';
        button.innerHTML = '<i class="fa fa-file-text-o"></i> Template';
        button.onclick = () => this.openTemplateDialog();
        toolbar.appendChild(button);
    }
    
    addLinkButton(toolbar) {
        const button = document.createElement('button');
        button.className = 'btn btn-sm btn-secondary';
        button.innerHTML = '<i class="fa fa-link"></i> Link';
        button.onclick = () => this.insertLink();
        toolbar.appendChild(button);
    }
    
    addImageButton(toolbar) {
        const button = document.createElement('button');
        button.className = 'btn btn-sm btn-secondary';
        button.innerHTML = '<i class="fa fa-image"></i> Image';
        button.onclick = () => this.insertImage();
        toolbar.appendChild(button);
    }
    
    addTableButton(toolbar) {
        const button = document.createElement('button');
        button.className = 'btn btn-sm btn-secondary';
        button.innerHTML = '<i class="fa fa-table"></i> Table';
        button.onclick = () => this.insertTable();
        toolbar.appendChild(button);
    }
    
    onContentChange() {
        // Handle content changes
        this.updateWordCount();
        this.autoSave();
    }
    
    updateWordCount() {
        const content = this.getContent();
        const wordCount = this.countWords(content);
        const wordCountElement = this.el.querySelector('.word-count');
        if (wordCountElement) {
            wordCountElement.textContent = `${wordCount} words`;
        }
    }
    
    countWords(content) {
        // Remove HTML tags and count words
        const plainText = content.replace(/<[^>]*>/g, '');
        const words = plainText.trim().split(/\s+/).filter(word => word.length > 0);
        return words.length;
    }
    
    autoSave() {
        // Auto-save functionality
        if (this.autoSaveTimeout) {
            clearTimeout(this.autoSaveTimeout);
        }
        this.autoSaveTimeout = setTimeout(() => {
            this.saveContent();
        }, 5000); // Auto-save after 5 seconds of inactivity
    }
    
    saveContent() {
        // Save content to the server
        const content = this.getContent();
        // Implementation depends on the form field integration
        console.log('Auto-saving content:', content);
    }
    
    getContent() {
        return this.editor.innerHTML || '';
    }
    
    setContent(content) {
        if (this.editor) {
            this.editor.innerHTML = content;
        }
    }
    
    openTemplateDialog() {
        // Open template selection dialog
        this.env.services.dialog.add('knowledge.template.dialog', {
            title: 'Insert Template',
            onSelect: (template) => {
                this.insertTemplate(template);
            }
        });
    }
    
    insertTemplate(template) {
        // Insert template content
        const content = this.getContent();
        const templateContent = template.body || '';
        this.setContent(content + templateContent);
    }
    
    insertLink() {
        // Insert link functionality
        const url = prompt('Enter URL:');
        const text = prompt('Enter link text:') || url;
        if (url) {
            const linkHtml = `<a href="${url}" target="_blank">${text}</a>`;
            this.insertHtml(linkHtml);
        }
    }
    
    insertImage() {
        // Insert image functionality
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'image/*';
        input.onchange = (event) => {
            const file = event.target.files[0];
            if (file) {
                this.uploadImage(file);
            }
        };
        input.click();
    }
    
    async uploadImage(file) {
        // Upload image to server
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            const response = await fetch('/knowledge/upload_image', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                const result = await response.json();
                const imageHtml = `<img src="${result.url}" alt="${result.name}" style="max-width: 100%; height: auto;">`;
                this.insertHtml(imageHtml);
            }
        } catch (error) {
            console.error('Image upload failed:', error);
        }
    }
    
    insertTable() {
        // Insert table functionality
        const rows = prompt('Number of rows:') || 3;
        const cols = prompt('Number of columns:') || 3;
        
        let tableHtml = '<table class="table table-bordered"><tbody>';
        for (let i = 0; i < rows; i++) {
            tableHtml += '<tr>';
            for (let j = 0; j < cols; j++) {
                tableHtml += '<td>&nbsp;</td>';
            }
            tableHtml += '</tr>';
        }
        tableHtml += '</tbody></table>';
        
        this.insertHtml(tableHtml);
    }
    
    insertHtml(html) {
        // Insert HTML at cursor position
        const selection = window.getSelection();
        if (selection.rangeCount > 0) {
            const range = selection.getRangeAt(0);
            const fragment = range.createContextualFragment(html);
            range.insertNode(fragment);
        } else {
            // If no selection, append to the end
            this.editor.innerHTML += html;
        }
    }
    
    onImageUpload(files) {
        // Handle image upload from editor
        files.forEach(file => {
            this.uploadImage(file);
        });
    }
}

// Register the component
registry.category("fields").add("knowledge_editor", KnowledgeEditor);