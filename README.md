# ProjT Launcher Meta by YONG Do-Hyun

Scripts to generate jsons and jars that ProjT Launcher will access.

## Recommended Deployment

Assuming you have a Flake-based NixOS configuration

- Add Flake input:

    ```nix
    {
      inputs.projt-meta.url = "github:Project-Tick/meta";
    }
    ```

- Import NixOS module and configure

    ```nix
    {inputs, ...}: {
      imports = [inputs.projt-meta.nixosModules.default];
      services.blockgame-meta = {
        enable = true;
        settings = {
          DEPLOY_TO_GIT = "true";
          GIT_AUTHOR_NAME = "Herpington Derpson";
          GIT_AUTHOR_EMAIL = "herpderp@derpmail.com";
          GIT_COMMITTER_NAME = "Herpington Derpson";
          GIT_COMMITTER_EMAIL = "herpderp@derpmail.com";
        };
      };
    }
    ```

- Rebuild and activate!
- Trigger it `systemctl start blockgame-meta.service`
- Monitor it `journalctl -fu blockgame-meta.service`
