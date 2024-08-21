
# [ch1] [note] anaconda报错
## 现象
```shell
~ conda activate your_environment
zsh: command not found: conda
```

由于我在不同电脑 （均为MacOS系统）上创造过Python运行环境，这是我用conda (anaconda3) 以来屡次遇见的报错。我以往的解决方式和大部分初见者一样简单粗暴——**删了，重装**。这次我偏犟上了，为什么，凭什么报错？

## 分析
我发现我安装的**不是 anaconda，而是 anaconda 的链接或替身。**
解决方案：
1. 在 访达/应用程序 中找到 conda ，右键显示简介，找到它的**原始项目**的安装路径。以我为例：它位于/opt/anaconda3/Anaconda-Navigator.app
2. 在访达中进入本地硬盘的**用户根目录**（~）。
3. 此时，你只能看到部分文件，hit Ctrl+Shift+. 以显示隐藏项目。（请记下这个快捷键，很容易忘记）
4. 找到文本文件“.zshrc”并用适当的文本编辑器打开。（我的终端用的是默认的 Z Shell，无论你用的是 Dracula 还是啥的，找它的配置文件即可）
5. 以我为例，根据安装路径，在 ~/.zshrc 中添加以下内容来设置 conda 的路径：

```shell
export PATH="$HOME/opt/anaconda3/bin:$PATH"
```

**但是，我犯了个错。**由于配置文件在 ~ 目录下，我想当然就认为我的 anaconda3 装在了我的用户目录下，可是别忘了，它的原始文件压根就没在硬盘上，opt 目录实际上在**根目录**（/）上。故此以上命令修改为：

```shell
export PATH="/opt/anaconda3/bin:$PATH"
```

6. 最后，初始化 conda并刷新：

```shell
conda init
source ~/.zshrc
```

**可是，问题又来了：**

```shell
 ~ conda init          
no change     /opt/anaconda3/condabin/conda
no change     /opt/anaconda3/bin/conda
no change     /opt/anaconda3/bin/conda-env
no change     /opt/anaconda3/bin/activate
no change     /opt/anaconda3/bin/deactivate
#此处省略几行......
No action taken.
```

我们需要手动添加 conda 初始化脚本到配置文件，包含**定义 Conda 环境的激活和停用方法**、**加载 Conda 环境变量**、**兼容不同的 shell**等等。
```shell
__conda_setup="$('/opt/anaconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/opt/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/opt/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/opt/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
```

再运行一遍 source ，问题就解决了。

## 后记
**Oh My Zsh** 很好用，可以显示目前所在分支，而且不同函数颜色不同，很醒目。

**以上问题或许只会发生在多用户电脑或曾经安装过 conda 的电脑上。**


