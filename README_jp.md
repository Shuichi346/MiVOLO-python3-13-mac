<div align="center">
<p>
   <a align="center" target="_blank">
   <img width="900" src="./images/MiVOLO.jpg"></a>
</p>
<br>
</div>



## MiVOLO: 年齢・性別推定のためのマルチ入力トランスフォーマー

> [**MiVOLO: 年齢・性別推定のためのマルチ入力トランスフォーマー**](https://arxiv.org/abs/2307.04616),
> Maksim Kuprashevich, Irina Tolstykh,
> *2023 [arXiv 2307.04616](https://arxiv.org/abs/2307.04616)*

> [**専門化を超えて：年齢・性別推定におけるMLLMの能力評価**](https://arxiv.org/abs/2403.02302),
> Maksim Kuprashevich, Grigorii Alekseenko, Irina Tolstykh
> *2024 [arXiv 2403.02302](https://arxiv.org/abs/2403.02302)*

[[`論文 2023`](https://arxiv.org/abs/2307.04616)] [[`論文 2024`](https://arxiv.org/abs/2403.02302)] [[`デモ`](https://huggingface.co/spaces/iitolstykh/age_gender_estimation_demo)] [[`🤗 HuggingFace`](https://huggingface.co/iitolstykh/mivolo_v2)] [[`🤗 HuggingFace 検出器`](https://huggingface.co/iitolstykh/YOLO-Face-Person-Detector)] [[`Telegram Bot`](https://t.me/AnyAgeBot)] [[`BibTex`](#citing)] [[`データ`](https://wildchlamydia.github.io/lagenda/)]

<div align="center">

<h2><sup>⚡ 新着</sup> MiVOLO-Next — 🤗 Spaces でライブデモ公開中</h2>

<p>
  <a href="https://huggingface.co/spaces/WildChlamydia/mivolo-next-demo"><img src="https://img.shields.io/badge/🤗%20Age%20%26%20Gender-Try%20it%20live-7c3aed?style=for-the-badge&labelColor=2D2240&logoColor=white" alt="年齢・性別デモ" height="44"></a>
  &nbsp;&nbsp;
  <a href="https://huggingface.co/spaces/WildChlamydia/mivolo-next-minor-demo"><img src="https://img.shields.io/badge/🤗%20Adult%20vs%20Minor-Try%20it%20live-c026d3?style=for-the-badge&labelColor=2D2240&logoColor=white" alt="成人 vs 未成年デモ" height="44"></a>
</p>

<sub>MiVOLO v2 の後継 — デュアルストリーム 顔 + 人物バックボーン · APPA-Real MAE 4.07 · A100 で 28,722 FPS</sub>

</div>

## MiVOLO 事前学習済みモデル

性別・年齢認識性能。

<table style="margin: auto">
  <tr>
    <th align="left">モデル</th>
    <th align="left" style="color:LightBlue">タイプ</th>
    <th align="left">データセット（学習・テスト）</th>
    <th align="left">年齢 MAE</th>
    <th align="left">年齢 CS@5</th>
    <th align="left">性別精度</th>
    <th align="left">ダウンロード</th>
  </tr>
  <tr>
    <td>volo_d1</td>
    <td align="left">顔のみ, 年齢</td>
    <td align="left">IMDB-cleaned</td>
    <td align="left">4.29</td>
    <td align="left">67.71</td>
    <td align="left">-</td>
    <td><a href="https://drive.google.com/file/d/17ysOqgG3FUyEuxrV3Uh49EpmuOiGDxrq/view?usp=drive_link">チェックポイント</a></td>
  </tr>
    <tr>
    <td>volo_d1</td>
    <td align="left">顔のみ, 年齢, 性別</td>
    <td align="left">IMDB-cleaned</td>
    <td align="left">4.22</td>
    <td align="left">68.68</td>
    <td align="left">99.38</td>
    <td><a href="https://drive.google.com/file/d/1NlsNEVijX2tjMe8LBb1rI56WB_ADVHeP/view?usp=drive_link">チェックポイント</a></td>
  </tr>
    <tr>
    <td>mivolo_d1</td>
    <td align="left">顔+身体, 年齢, 性別</td>
    <td align="left">IMDB-cleaned</td>
    <td align="left">4.24 [顔+身体]<br>6.87 [身体]</td>
    <td align="left">68.32 [顔+身体]<br>46.32 [身体]</td>
    <td align="left">99.46 [顔+身体]<br>96.48 [身体]</td>
    <td><a href="https://drive.google.com/file/d/11i8pKctxz3wVkDBlWKvhYIh7kpVFXSZ4/view?usp=drive_link">model_imdb_cross_person_4.24_99.46.pth.tar</a></td>
  </tr>
  <tr>
    <td>volo_d1</td>
    <td align="left">顔のみ, 年齢</td>
    <td align="left">UTKFace</td>
    <td align="left">4.23</td>
    <td align="left">69.72</td>
    <td align="left">-</td>
    <td><a href="https://drive.google.com/file/d/1LtDfAJrWrw-QA9U5IuC3_JImbvAQhrJE/view?usp=drive_link">チェックポイント</a></td>
  </tr>
    <tr>
    <td>volo_d1</td>
    <td align="left">顔のみ, 年齢, 性別</td>
    <td align="left">UTKFace</td>
    <td align="left">4.23</td>
    <td align="left">69.78</td>
    <td align="left">97.69</td>
    <td><a href="https://drive.google.com/file/d/1hKFmIR6fjHMevm-a9uPEAkDLrTAh-W4D/view?usp=drive_link">チェックポイント</a></td>
  </tr>
  <tr>
    <td>mivolo_d1</td>
    <td align="left">顔+身体, 年齢, 性別</td>
    <td align="left">Lagenda</td>
    <td align="left">3.99 [顔+身体]</td>
    <td align="left">71.27 [顔+身体]</td>
    <td align="left">97.36 [顔+身体]</td>
    <td><a href="https://huggingface.co/spaces/iitolstykh/demo">デモ</a></td>
  </tr>
  <tr>
    <td>mivolov2_d1_384x384</td>
    <td align="left">顔+身体, 年齢, 性別</td>
    <td align="left">Lagenda</td>
    <td align="left">3.65 [顔+身体]</td>
    <td align="left">74.48 [顔+身体]</td>
    <td align="left">97.99 [顔+身体]</td>
    <td> <a href="https://huggingface.co/iitolstykh/mivolo_v2">チェックポイント</a> <br> <a href="https://t.me/AnyAgeBot">Telegram Bot</a> </td>
  </tr>

</table>

## MiVOLO 回帰ベンチマーク

性別・年齢認識性能。

[valid_age_gender.sh](scripts/valid_age_gender.sh) を使用して、チェックポイントで結果を再現してください。

<table style="margin: auto">
  <tr>
    <th align="left">モデル</th>
    <th align="left" style="color:LightBlue">タイプ</th>
    <th align="left">学習データセット</th>
    <th align="left">テストデータセット</th>
    <th align="left">年齢 MAE</th>
    <th align="left">年齢 CS@5</th>
    <th align="left">性別精度</th>
    <th align="left">ダウンロード</th>
  </tr>

  <tr>
    <td>mivolo_d1</td>
    <td align="left">顔+身体, 年齢, 性別</td>
    <td align="left">Lagenda</td>
    <td align="left">AgeDB</td>
    <td align="left">5.55 [顔]</td>
    <td align="left">55.08 [顔]</td>
    <td align="left">98.3 [顔]</td>
    <td><a href="https://huggingface.co/spaces/iitolstykh/demo">デモ</a></td>
  </tr>
  <tr>
    <td>mivolo_d1</td>
    <td align="left">顔+身体, 年齢, 性別</td>
    <td align="left">IMDB-cleaned</td>
    <td align="left">AgeDB</td>
    <td align="left">5.58 [顔]</td>
    <td align="left">55.54 [顔]</td>
    <td align="left">97.93 [顔]</td>
    <td><a href="https://drive.google.com/file/d/11i8pKctxz3wVkDBlWKvhYIh7kpVFXSZ4/view?usp=drive_link">model_imdb_cross_person_4.24_99.46.pth.tar</a></td>
  </tr>

</table>

## MiVOLO 分類ベンチマーク

性別・年齢認識性能。

<table style="margin: auto">
  <tr>
    <th align="left">モデル</th>
    <th align="left" style="color:LightBlue">タイプ</th>
    <th align="left">学習データセット</th>
    <th align="left">テストデータセット</th>
    <th align="left">年齢精度</th>
    <th align="left">性別精度</th>
  </tr>

  <tr>
    <td>mivolo_d1</td>
    <td align="left">顔+身体, 年齢, 性別</td>
    <td align="left">Lagenda</td>
    <td align="left">FairFace</td>
    <td align="left">61.07 [顔+身体]</td>
    <td align="left">95.73 [顔+身体]</td>
  </tr>
  <tr>
    <td>mivolo_d1</td>
    <td align="left">顔+身体, 年齢, 性別</td>
    <td align="left">Lagenda</td>
    <td align="left">Adience</td>
    <td align="left">68.69 [顔]</td>
    <td align="left">96.51 [顔]</td>
  </tr>
  <tr>
    <td>mivolov2_d1_384</td>
    <td align="left">顔+身体, 年齢, 性別</td>
    <td align="left">Lagenda</td>
    <td align="left">Adience</td>
    <td align="left">69.43 [顔]</td>
    <td align="left">97.39 [顔]</td>
  </tr>

</table>

## データセット

**このデータを使用する場合は、[論文を引用](#citing)してください！**

- Lagenda データセット: [画像](https://drive.google.com/file/d/1QXO0NlkABPZT6x1_0Uc2i6KAtdcrpTbG/view?usp=sharing) と [アノテーション](https://drive.google.com/file/d/1mNYjYFb3MuKg-OL1UISoYsKObMUllbJx/view?usp=sharing)。
- IMDB-clean: 画像の取得は [こちらの手順](https://github.com/yiminglin-ai/imdb-clean) に従い、アノテーションは [ダウンロード](https://drive.google.com/file/d/17uEqyU3uQ5trWZ5vRJKzh41yeuDe5hyL/view?usp=sharing) してください。
- UTK データセット: [オリジナル全画像](https://susanqq.github.io/UTKFace/) と アノテーション: [論文のスプリット](https://drive.google.com/file/d/1Fo1vPWrKtC5bPtnnVWNTdD4ZTKRXL9kv/view?usp=sharing)、[ランダム全スプリット](https://drive.google.com/file/d/177AV631C3SIfi5nrmZA8CEihIt29cznJ/view?usp=sharing)。
- Adience データセット: 画像の取得は [こちらの手順](https://talhassner.github.io/home/projects/Adience/Adience-data.html) に従い、アノテーションは [ダウンロード](https://drive.google.com/file/d/1wS1Q4FpksxnCR88A1tGLsLIr91xHwcVv/view?usp=sharing) してください。
   <details>
      <summary>クリックして展開！</summary>

   ダウンロード後、`data` ディレクトリは以下のような構成になります：

   ```console
   data
   └── Adience
       ├── annotations  (アノテーションフォルダ)
       ├── aligned      (使用しません)
       ├── faces
       ├── fold_0_data.txt
       ├── fold_1_data.txt
       ├── fold_2_data.txt
       ├── fold_3_data.txt
       └── fold_4_data.txt
   ```

   `faces/` ディレクトリの粗く整列された画像を使用します。

   検出器を使用して各画像の顔バウンディングボックスを検出しました（[tools/prepare_adience.py](tools/prepare_adience.py) を参照）。

   このデータセットには5つのフォールドがあります。性能指標は5分割交差検証での精度です。

   | 削除前の画像数 | fold 0 | fold 1 | fold 2 | fold 3 | fold 4 |
   | -------------- | ------ | ------ | ------ | ------ | ------ |
   | 19,370         | 4,484  | 3,730  | 3,894  | 3,446  | 3,816  |

   不完全なデータ

   | 年齢のみ未検出 | 性別のみ未検出 | 合計           |
   | -------------- | -------------- | -------------- |
   | 40             | 1170           | 1,210 (6.2 %) |

   削除されたデータ

   | 画像処理失敗 | 年齢・性別ともに未検出 | 合計         |
   | ------------ | ---------------------- | ------------ |
   | 0            | 708                    | 708 (3.6 %) |

   性別

   | 女性   | 男性  |
   | ------ | ----- |
   | 9,372  | 8,120 |

   年齢（8クラス）— 非重複年齢区間へのマッピング後

   | 0-2   | 4-6   | 8-12  | 15-20 | 25-32 | 38-43 | 48-53 | 60-100 |
   | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ------ |
   | 2,509 | 2,140 | 2,293 | 1,791 | 5,589 | 2,490 | 909   | 901    |

   </details>

- FairFace データセット: 画像の取得は [こちらの手順](https://github.com/joojs/fairface) に従い、アノテーションは [ダウンロード](https://drive.google.com/file/d/1EdY30A1SQmox96Y39VhBxdgALYhbkzdm/view?usp=drive_link) してください。
    <details>
      <summary>クリックして展開！</summary>

    ダウンロード後、`data` ディレクトリは以下のような構成になります：

    ```console
    data
    └── FairFace
       ├── annotations  (アノテーションフォルダ)
       ├── fairface-img-margin025-trainval   (使用しません)
           ├── train
           ├── val
       ├── fairface-img-margin125-trainval
           ├── train
           ├── val
       ├── fairface_label_train.csv
       ├── fairface_label_val.csv

    ```

    `fairface-img-margin125-trainval/` ディレクトリの整列済み画像を使用します。

    検出器を使用して各画像の顔バウンディングボックスを検出し、可能な場合は人物バウンディングボックスも追加しました（[tools/prepare_fairface.py](tools/prepare_fairface.py) を参照）。

    このデータセットには train と val の2つのスプリットがあります。性能指標は検証データでの精度です。

    | 学習画像数 | 検証画像数 |
    | ---------- | ---------- |
    | 86,744     | 10,954     |

    **検証データ**の性別

    | 女性   | 男性  |
    | ------ | ----- |
    | 5,162  | 5,792 |

    **検証データ**の年齢（9クラス）：

    | 0-2 | 3-9   | 10-19 | 20-29 | 30-39 | 40-49 | 50-59 | 60-69 | 70+ |
    | --- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | --- |
    | 199 | 1,356 | 1,181 | 3,300 | 2,330 | 1,353 | 796   | 321   | 118 |

    </details>
- AgeDB データセット: 画像の取得は [こちらの手順](https://ibug.doc.ic.ac.uk/resources/agedb/) に従い、アノテーションは [ダウンロード](https://drive.google.com/file/d/1Dp72BUlAsyUKeSoyE_DOsFRS1x6ZBJen/view) してください。
    <details>
      <summary>クリックして展開！</summary>

  **年齢**: 1 - 101

  **性別**: `M` の顔 9,788 枚、`F` の顔 6,700 枚

  | 画像 0 | 画像 1 | 画像 2 | 画像 3 | 画像 4 | 画像 5 | 画像 6 | 画像 7 | 画像 8 | 画像 9 |
  |--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
  | 1701   | 1721   | 1615   | 1619   | 1626   | 1643   | 1634   | 1596   | 1676   | 1657   |

    データスプリットは [こちら](https://github.com/paplhjak/Facial-Age-Estimation-Benchmark-Databases) から取得しました。

    !! **全スプリット（全データセット）をモデル評価に使用しました。**
    </details>

## インストール

このフォークには Python 3.13 以降が必要で、プロジェクト環境に [uv](https://docs.astral.sh/uv/) を使用します。
チェックアウト直後から：

```bash
uv sync
```

uv は `.python-version` を読み込み、リポジトリローカルの `.venv` を作成し、`uv.lock` に記載された正確なバージョンをインストールします。
プロジェクトのコマンドは `uv run` で実行してください。手動でのアクティベーションは不要です。

パッケージは `pyproject.toml` の宣言的な PEP 517 メタデータを使用するようになりました。Git インストールはメタデータ生成の失敗を引き起こしていた旧来の `pkg_resources` 依存関係パーサーを実行しなくなりました。`requirements.txt` はプロジェクトメタデータへの互換性ポインタとしてのみ残ります。

## Gradio GUI

ローカルの Gradio 6 インターフェースを起動するには：

```bash
uv run mivolo-gui
```

[http://127.0.0.1:7860](http://127.0.0.1:7860) を開き、画像をアップロードして **推論を実行** を選択します。サーバーはデフォルトで `127.0.0.1` にバインドされており、他のコンピューターには公開されません。

初回推論時、GUI は公式のバージョン固定済み Hugging Face リポジトリスナップショットから、ドキュメント記載の検出器とレガシー MiVOLO v2 チェックポイントをダウンロードします。ファイルは Hugging Face キャッシュ（通常 `~/.cache/huggingface/hub` 以下）から再利用されます。公開デフォルトはアカウント不要です。環境で認証済みの Hub アクセスが必要な場合のみ `HF_TOKEN` を設定してください。

デバイスセレクターのデフォルトは `auto` で、Apple MPS を優先し、CPU にフォールバックします。どちらも完全精度で実行されます。PyTorch がサポートされていない MPS 操作を報告する場合は、CPU を明示的に選択してください。

任意のローカルモデルフィールドは、通常のパス、Finder でクォートされたパス、スペースがエスケープされたターミナルパスを受け付けます。PyTorch および Ultralytics のウェイトファイルには実行可能な pickle データが含まれる可能性があるため、信頼できるカスタム `.pt` または `.pth.tar` ファイルのみを選択してください。

## コマンドラインデモ

1. 身体+顔の検出器モデルを `models/yolov8x_person_face.pt` に [ダウンロード](https://drive.google.com/file/d/1CGNCkZQNj5WkP3rLpENWAOgrBQkUWRdw/view) します。
2. mivolo チェックポイントを `models/mivolo_imbd.pth.tar` に [ダウンロード](https://drive.google.com/file/d/11i8pKctxz3wVkDBlWKvhYIh7kpVFXSZ4/view) します。

```bash
uv run mivolo-cli \
--input "jennifer_lawrence.jpg" \
--output "output" \
--detector-weights "models/yolov8x_person_face.pt" \
--checkpoint "models/mivolo_imbd.pth.tar" \
--device "auto" \
--with-persons \
--draw
```

元のエントリポイントは `uv run python demo.py` として同じ引数で引き続き利用可能です。

YouTube 動画を処理するには：

```bash
uv run mivolo-cli \
--input "https://www.youtube.com/shorts/pVh32k0hGEI" \
--output "output" \
--detector-weights "models/yolov8x_person_face.pt" \
--checkpoint "models/mivolo_imbd.pth.tar" \
--device "auto" \
--draw \
--with-persons
```


## 検証

検証メトリクスを再現するには：

1. imbd-clean / utk / adience / lagenda / fairface の準備済みアノテーションをダウンロードします。
2. チェックポイントをダウンロードします。
3. 検証を実行します：

```bash
uv run python eval_pretrained.py \
  --dataset_images /path/to/dataset/utk/images \
  --dataset_annotations /path/to/dataset/utk/annotation \
  --dataset_name utk \
  --split valid \
  --batch-size 512 \
  --checkpoint models/mivolo_imbd.pth.tar \
  --with-persons \
  --device "cpu"
```

サポートされているデータセット名: "utk"、"imdb"、"lagenda"、"fairface"、"adience"。


## 変更履歴

[CHANGELOG.md](CHANGELOG.md)

## ONNX および TensorRT エクスポート

現時点（2023年8月11日）では、ONNX エクスポートは技術的には可能ですが、バッチ処理での出力モデルの性能が低いため推奨されません。
**TensorRT** および **OpenVINO** エクスポートは、col2im のサポートがないため不可能です。

どうしても ONNX エクスポートを使用する場合は、[こちらの手順](https://github.com/WildChlamydia/MiVOLO/issues/14#issuecomment-1675245889) を参照してください。

現時点で最も推奨されるエクスポート方法は **TorchScript の使用** です。以下の1行のコードで実現できます：
```python
torch.jit.trace(model)
```
このアプローチにより、元の速度を維持したモデルが得られ、使用に必要なファイルが1つだけとなり、追加コードが不要になります。

## ライセンス

[こちら](LICENSE) を参照してください。


## 引用

モデル、コード、またはデータセットを使用する場合は、以下の論文を引用し、リポジトリに :star: を付けていただけると幸いです。

```bibtex
@article{mivolo2023,
   Author = {Maksim Kuprashevich and Irina Tolstykh},
   Title = {MiVOLO: Multi-input Transformer for Age and Gender Estimation},
   Year = {2023},
   Eprint = {arXiv:2307.04616},
}
```
```bibtex
@article{mivolo2024,
   Author = {Maksim Kuprashevich and Grigorii Alekseenko and Irina Tolstykh},
   Title = {Beyond Specialization: Assessing the Capabilities of MLLMs in Age and Gender Estimation},
   Year = {2024},
   Eprint = {arXiv:2403.02302},
}
```
