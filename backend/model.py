import torch
import torch.nn as nn
from transformers import AutoModel

class RoBERTaClassifier(nn.Module):
    def __init__(self):
        super(RoBERTaClassifier, self).__init__()
        self.roberta = AutoModel.from_pretrained("roberta-base")
        
        # Fine-tune only the last two transformer layers and pooler
        for name, param in self.roberta.named_parameters():
            if "encoder.layer.10" in name or "encoder.layer.11" in name or "pooler" in name:
                param.requires_grad = True
            else:
                param.requires_grad = False

        self.dropout = nn.Dropout(0.3)
        self.classifier = nn.Sequential(
            nn.Linear(768, 512),
            nn.BatchNorm1d(512),
            nn.GELU(),
            nn.Dropout(0.3),
            nn.Linear(512, 2)
        )

    def forward(self, input_ids, attention_mask):
        outputs = self.roberta(input_ids=input_ids, attention_mask=attention_mask, return_dict=True)
        x = outputs.last_hidden_state[:, 0, :]  # CLS token
        return self.classifier(x)
