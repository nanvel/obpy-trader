# Deploy

```bash
pip install ansible==3.2
```

```bash
ansible-playbook ansible/setup_user.yml -i ansible/production -u ubuntu --vault-password-file local_secret.txt --private-key local_ssh.pem
```
