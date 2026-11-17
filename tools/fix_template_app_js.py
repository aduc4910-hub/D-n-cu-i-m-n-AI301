import re

with open('tools/generate_navy_blue_app_js.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the loadQuickQuestionTemplate section
pattern_tpl = re.compile(r'function loadQuickQuestionTemplate\(type\)\s*\{.*?\}\s*\}', re.DOTALL)
correct_template = '''function loadQuickQuestionTemplate(type) {
  currentBusinessContext = {
    company_type: "Bán lẻ & Thương mại điện tử (Omnichannel)",
    industry: "Thiết bị Công nghệ & Điện tử thông minh",
    time_scope: "Năm tài chính 2025 (12 tháng)",
    additional_notes: "Đánh giá hiệu quả 5 kênh bán và danh mục sản phẩm chính 4 quý năm 2025.",
    questions: [
      "Doanh thu theo kênh bán hàng nào cao nhất?",
      "Sản phẩm nào mang lại lợi nhuận cao nhất?",
      "Chi phí chiết khấu ảnh hưởng thế nào đến biên lợi nhuận?"
    ]
  };
  const typeEl = document.getElementById('ctx-company-type');
  const notesEl = document.getElementById('ctx-notes-input');
  const questionsEl = document.getElementById('ctx-questions-input');
  if (typeEl) typeEl.value = currentBusinessContext.company_type;
  if (notesEl) notesEl.value = currentBusinessContext.additional_notes;
  if (questionsEl) questionsEl.value = currentBusinessContext.questions.join('\\\\n');
}'''

text = pattern_tpl.sub(correct_template, text)

# Also ensure we don't have double closing braces anywhere around it
text = text.replace("questions.join('\\n');\n}\n}", "questions.join('\\\\n');\n}")
text = text.replace("questions.join('\n');\n}\n}", "questions.join('\\\\n');\n}")

with open('tools/generate_navy_blue_app_js.py', 'w', encoding='utf-8') as f:
    f.write(text)

with open('tools/generate_glass_app_js.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed loadQuickQuestionTemplate successfully!")
