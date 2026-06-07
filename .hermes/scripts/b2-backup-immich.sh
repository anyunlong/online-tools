#!/bin/bash
# Immich 照片 + 数据库每周备份 → B2（异步后台模式）
# 触发：每周日 03:00，秒级退出

export PATH="/Users/anyunlong/Library/Python/3.9/bin:$PATH"
B2_BUCKET="immich-anyunlong-backup"
SYNC_LOG="/tmp/b2-weekly-sync.log"
IMMICH_LOG="/tmp/b2-weekly-immich.log"

echo "=== Immich 每周备份 $(date) ==="

# 检查上次结果
if [ -f "$SYNC_LOG" ]; then
    LAST_RESULT=$(tail -1 "$SYNC_LOG" 2>/dev/null)
    if echo "$LAST_RESULT" | grep -q "OK"; then
        echo "  ✅ 上周备份成功"
    elif echo "$LAST_RESULT" | grep -q "FAIL"; then
        echo "  ❌ 上周备份失败，查看 $IMMICH_LOG"
    fi
else
    echo "  📋 首次运行"
fi

# 后台同步
rm -f "$IMMICH_LOG"

(
    set +e
    OK=true

    # 数据库备份
    echo "[$(date)] 数据库备份同步中..." >> "$IMMICH_LOG"
    b2 sync --delete \
        "/Users/anyunlong/immich/library/backups" \
        "b2://${B2_BUCKET}/library/backups" \
        2>&1 | grep -v "urllib3\|NotOpenSSL\|warnings.warn" >> "$IMMICH_LOG" 2>&1
    RC=${PIPESTATUS[0]}
    if [ "$RC" -ne 0 ]; then
        echo "  ⚠️ 数据库备份退出码 $RC" >> "$IMMICH_LOG"
        OK=false
    fi

    # 原始照片
    echo "[$(date)] upload/ 同步中..." >> "$IMMICH_LOG"
    b2 sync --delete --replace-newer \
        "/Volumes/Seagate Exp/immich/upload/" \
        "b2://${B2_BUCKET}/library/upload" \
        2>&1 | grep -v "urllib3\|NotOpenSSL\|warnings.warn" >> "$IMMICH_LOG" 2>&1
    RC=${PIPESTATUS[0]}
    if [ "$RC" -ne 0 ]; then
        echo "  ⚠️ upload/ 同步退出码 $RC" >> "$IMMICH_LOG"
        OK=false
    fi

    if $OK; then
        echo "OK $(date)" >> "$SYNC_LOG"
        echo "  ✅ Immich 同步完成 $(date)" >> "$IMMICH_LOG"
    else
        echo "FAIL $(date)" >> "$SYNC_LOG"
        echo "  ❌ Immich 同步失败 $(date)" >> "$IMMICH_LOG"
    fi
) > /dev/null 2>&1 &

echo "  ⏳ 后台同步中...（首次可能数小时，后续增量较快）"
echo "=== $(date) 完成 ==="
