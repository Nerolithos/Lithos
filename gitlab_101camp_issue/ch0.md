# [ch0] [note] 关于信息同步、合并与冲突

这是我第一次尝试发起issue，起因是这样的：
在试图编辑 /tasks/wikis 的 sidebar 中的 manifesto 时，我发现用户 sunnyseed 为我预留了“席位”来提醒我如何编辑它、给它接上链接之类的。而我本地的wikis是在他编辑之前克隆的。
这只是需要合并而已，我以为。于是我在本地编辑了wikis，然后开始试图push。

```shell
➜  Lithos ls
7py        tasks.wiki
➜  Lithos cd tasks.wiki
➜  tasks.wiki git:(master) git status
On branch master
Your branch is up to date with 'origin/master'.

nothing to commit, working tree clean
```

首先，“working tree clean” 说明没有待 push 的项目。然而，我最开始以为是本地与远程没有差别。
事实上，从上行角度看，git status 检查的是本地仓库中文件是否已暂存(git add)？或者是否已提交(git commit -m …)？从下行角度看，它只会将当前仓库与你上一次 fetch 或pull 下来的仓库进行同步检查。
它与远程仓库没有直接关联，所以也不用期待它能魔法般地帮你 cat 一眼，此时此刻，本地与远程有没有信息差。

```shell
➜  tasks.wiki git:(master) git remote update

remote: Enumerating objects: 4, done.
remote: Counting objects: 100% (4/4), done.
remote: Compressing objects: 100% (4/4), done.
remote: Total 4 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
Unpacking objects: 100% (4/4), 3.76 KiB | 962.00 KiB/s, done.
From https://gitlab.com/101camp/7py/tasks.wiki
   d825bd4..6ae23af  master     -> origin/master
➜  tasks.wiki git:(master) 
➜  tasks.wiki git:(master) git status       
On branch master
Your branch is behind 'origin/master' by 1 commit, and can be fast-forwarded.
  (use "git pull" to update your local branch)

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
 modified:   _sidebar.md

no changes added to commit (use "git add" and/or "git commit -a")
```

为了我自己能够看得懂，这里展示了 git 的底层逻辑（最基础的那些功能）。

![](%5Bch0%5D%20%5Bnote%5D%20%E5%85%B3%E4%BA%8E%E4%BF%A1%E6%81%AF%E5%90%8C%E6%AD%A5%E3%80%81%E5%90%88%E5%B9%B6%E4%B8%8E%E5%86%B2%E7%AA%81/8B86991E-5178-48A0-B037-7E71B735201D.jpg)
（图中的 Index 代表暂存区域 Staging Area）

我们发现，在 git remote update 之前的 “clean” 变成了 “behind” ，也就是本地仓库中出现的超越工作区的一个 wikis 的“新版本”，也就是 sunnyseed创造出的版本被拉下来了。
“git remote update”会取下所有远程仓库所有分支中的信息放到本地仓库；而git fetch可以获取特定分支的最新信息。也就是说，前者是地图炮而后者是精确制导。“git fetch <远程仓库><远程分支>”将远程主机的最新内容拉到本地，用户在检查了以后决定是否合并到工作本机分支中（git merge<远程分支>)。
而“git pull <远程仓库><远程分支>”则是将远程主机的最新内容拉下来后直接合并，即：git pull = git fetch , git remote update + git merge，这样可能会在合并时产生冲突，需要手动解决。（远程仓库默认为origin，远程分支可以是master，或用户名分支。）
然而我忘记了 merge 。于是，问题等会就出现了。

```shell
➜  tasks.wiki git:(master) ✗ git add _sidebar.md
➜  tasks.wiki git:(master) ✗ git commit -a "#3"
fatal: paths '#3 ...' with -a does not make sense
➜  tasks.wiki git:(master) ✗ git commit -m "#3"
[master 7e7f8ba] #3
 1 file changed, 3 insertions(+), 1 deletion(-)
```

顺带记录，-a 和 -m 是 commit 的选项，-a 可以代替 git add 的功能，而 -m 是常用的在命令行中提交信息。以上乱糟糟的一团归结起来就是一句 git commit -a -m “#3”。

```shell
➜  tasks.wiki git:(master) git push
To https://gitlab.com/101camp/7py/tasks.wiki.git
 ! [rejected]        master -> master (non-fast-forward)
error: failed to push some refs to 'https://gitlab.com/101camp/7py/tasks.wiki.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. If you want to integrate the remote changes,
hint: use 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
➜  tasks.wiki git:(master) git pull origin master
From https://gitlab.com/101camp/7py/tasks.wiki
* branch            master     -> FETCH_HEAD
hint: You have divergent branches and need to specify how to reconcile them.
hint: You can do so by running one of the following commands sometime before
hint: your next pull:
hint:
hint:   git config pull.rebase false  # merge
hint:   git config pull.rebase true   # rebase
hint:   git config pull.ff only       # fast-forward only
hint:
hint: You can replace "git config" with "git config --global" to set a default
hint: preference for all repositories. You can also pass --rebase, --no-rebase,
hint: or --ff-only on the command line to override the configured default per
hint: invocation.
fatal: Need to specify how to reconcile divergent branches.
```

这里暴露了 git pull 简洁灵活背后的小问题。首先，当我试图将我的版本 push 出去时，由于本地仓库存在远程仓库的新信息（刚才 update 的），所以推不出去。
当我试图先 pull 再 push 时，需要提供合并方案。其中， rebase 会将两个分支“首尾相接”合二为一，并去除提交历史：而 merge 则会保留两者的历史记录。

```shell
➜  tasks.wiki git:(master) git pull origin master --no-rebase
From https://gitlab.com/101camp/7py/tasks.wiki
* branch            master     -> FETCH_HEAD
Auto-merging _sidebar.md
CONFLICT (content): Merge conflict in _sidebar.md
Automatic merge failed; fix conflicts and then commit the result.
➜  tasks.wiki git:(master) ✗ git add _sidebar.md
➜  tasks.wiki git:(master) ✗ git commit -m "Resolved merge conflict in _sidebar.md"
[master f57693d] Resolved merge conflict in _sidebar.md
➜  tasks.wiki git:(master) git push
Enumerating objects: 10, done.
Counting objects: 100% (10/10), done.
Delta compression using up to 8 threads
Compressing objects: 100% (6/6), done.
Writing objects: 100% (6/6), 639 bytes | 639.00 KiB/s, done.
Total 6 (delta 4), reused 0 (delta 0), pack-reused 0 (from 0)
To https://gitlab.com/101camp/7py/tasks.wiki.git
   6ae23af..f57693d  master -> master
```

最后，我手动在文本编辑器里合并了两个分支（其实就是直接删除了一部分），并推到远程仓库。

我的问题是，既然 merge 会“保留历史”，我应当如何翻阅这个记录呢？因为合并过程不在远程，我不可能在 gitlab 的 tasks 的 UI 界面上的“历史”栏目找到它。
（待补充）