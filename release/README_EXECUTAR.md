# Como executar o Dev_Mode

## Arquivos necessários (na mesma pasta)

- `dev_mode.AppImage`
- `dev_mode.desktop`
- `launch_dev_mode.sh`
- `dev_mode.png`

## Passos

1. **Baixe todos os arquivos** e coloque-os na **mesma pasta**.

2. **Dê permissão de execução** (abra o terminal na pasta e rode):
   ```bash
   chmod +x dev_mode.AppImage launch_dev_mode.sh dev_mode.desktop
   ```

3. **Duplo clique** no `dev_mode.desktop`.
   - Se aparecer aviso de segurança, clique com botão direito → **Propriedades** → marque como confiável, depois abra.

Pronto! O Dev Mode vai iniciar sem precisar instalar Python ou dependências.

---

> **Dica:** Você pode mover a pasta inteira para qualquer lugar — ela é portável. O atalho funciona de qualquer diretório, desde que os 4 arquivos estejam juntos.