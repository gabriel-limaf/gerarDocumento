# uvicorn main:app --reload
# abrir local para testar a API http://localhost:8000/docs
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from docx import Document
import os
import sqlite3

app = FastAPI()

# Conexão com o banco de dados persistente
conn = sqlite3.connect('pessoas.db', check_same_thread=False)
cursor = conn.cursor()


# Função para preencher o documento com os dados
def fill_docx(template_path: str, output_path: str, data: dict):
    doc = Document(template_path)
    for paragraph in doc.paragraphs:
        for key, value in data.items():
            if key in paragraph.text:
                paragraph.text = paragraph.text.replace(key, value)
    doc.save(output_path)


# Função para buscar dados no banco de dados pelo CPF
def get_data_by_cpf(cpf: str):
    cursor.execute('SELECT name, email, age, city, state, country, cpf FROM persons WHERE cpf = ?', (cpf,))
    row = cursor.fetchone()
    if row:
        return {
            "{{Nome}}": row[0],
            "{{Email}}": row[1],
            "{{Idade}}": str(row[2]),
            "{{Cidade}}": row[3],
            "{{Estado}}": row[4],
            "{{País}}": row[5],
            "{{CPF}}": row[6],
        }
    else:
        return None


@app.post("/fill-doc/")
async def fill_doc(file: UploadFile = File(...), cpf: str = Form(...)):
    # Buscar os dados no banco pelo CPF
    data = get_data_by_cpf(cpf)
    if not data:
        raise HTTPException(status_code=404, detail="CPF não encontrado no banco de dados")

    # Salvar o arquivo carregado
    input_path = os.path.join("files", file.filename)
    os.makedirs(os.path.dirname(input_path), exist_ok=True)
    with open(input_path, "wb") as f:
        f.write(file.file.read())

    # Definir o caminho de saída
    output_path = os.path.join("files", f"filled_{file.filename}")

    # Preencher o documento com os dados do banco
    fill_docx(input_path, output_path, data)

    # Retornar o documento preenchido
    return FileResponse(output_path, filename=f"filled_{file.filename}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

