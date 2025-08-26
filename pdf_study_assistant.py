import dashscope
import PyPDF2
import gradio as gr

# ----------------------------
# 1. 填写你的 API Key
# ----------------------------
dashscope.api_key = "#######"

# ----------------------------
# 2. 处理 PDF 并生成总结函数
# ----------------------------
def summarize_pdf(file):
    pdf_text = ""
    reader = PyPDF2.PdfReader(file.name)
    for page in reader.pages:
        pdf_text += page.extract_text() + "\n"

    prompt = f"请阅读下面内容，并帮我总结出重点考点：\n{pdf_text}"

    response = dashscope.Generation.call(
        model="qwen-turbo",
        prompt=prompt
    )

    summary = response["output"]["text"]
    return summary

# ----------------------------
# 3. 创建 Gradio 界面
# ----------------------------
with gr.Blocks() as demo:
    gr.Markdown("# 📚 学习助手 AI")
    gr.Markdown("上传课程 PDF，自动生成重点考点总结。")

    with gr.Row():
        pdf_file = gr.File(label="选择 PDF 文件", file_types=[".pdf"])
        summarize_btn = gr.Button("生成总结")

    summary_output = gr.Textbox(label="AI 生成的总结", lines=15)

    # 绑定按钮点击事件
    summarize_btn.click(fn=summarize_pdf, inputs=pdf_file, outputs=summary_output)

# ----------------------------
# 4. 运行界面
# ----------------------------
demo.launch()

