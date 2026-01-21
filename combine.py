# 阶段三：合并结果并生成最终产物
  combine:
    needs: process # 等待所有 process 任务都完成后再开始
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: 3.8

      # --- 添加这个缺失的步骤 ---
      - name: Install dependencies
        run: pip install -r requirements.txt
      # ---------------------------

      - name: Download all processed chunks and base data
        # 不指定 name 会下载本次工作流的所有 artifacts
        uses: actions/download-artifact@v4
        with:
          path: . # 下载到当前目录

      - name: (Step 3a) Combine all chunks
        run: python combine.py
      
      - name: (Step 3b) Build HTML
        run: python generate_html.py
      
      - name: (Step 3c) Build CSV
        run: python generate_csv.py

      - name: Upload final output file
        uses: actions/upload-artifact@v4
        with:
          name: Output
          path: |
            takeout.json
            takeout.html
            takeout*.csv
